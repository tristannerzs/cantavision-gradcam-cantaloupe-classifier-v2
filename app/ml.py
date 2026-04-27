from __future__ import annotations
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from .settings import MODELS_DIR, CONFIG, IMAGE_SIZE
_TF=None; _KERAS=None; _MODEL=None; _MODEL_PATH: Path|None=None
ALLOWED_IMAGE_EXTS={'.jpg','.jpeg','.png','.bmp','.webp'}
@dataclass
class PredictionOutput:
    model_name: str; predicted_label: str; probability_cantaloupe: float; probability_not_cantaloupe: float; confidence: float; threshold: float; gradcam_status: str; gradcam_layer: str; note: str; crop: Image.Image; heatmap_block: Image.Image; heatmap_smooth: Image.Image; overlay: Image.Image; study: Image.Image; roi: dict[str,int]
def lazy_tf():
    global _TF,_KERAS
    if _TF is None:
        import tensorflow as tf
        from tensorflow import keras
        _TF=tf; _KERAS=keras
    return _TF,_KERAS
def model_files():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    files=[]
    for pat in ('*.keras','*.h5','*.hdf5'): files.extend(MODELS_DIR.glob(pat))
    pref=CONFIG.get('model_filename','cantaloupe_model.keras')
    return sorted(files, key=lambda p:(p.name!=pref,p.name.lower()))
def choose_model_path():
    preferred=MODELS_DIR/str(CONFIG.get('model_filename','cantaloupe_model.keras'))
    if preferred.exists(): return preferred
    files=model_files(); return files[0] if files else None
def load_model(force=False):
    global _MODEL,_MODEL_PATH
    path=choose_model_path()
    if path is None:
        _MODEL=None; _MODEL_PATH=None
        return {'ok':False,'message':'No model found. Put your trained Keras file at models/cantaloupe_model.keras.','model':None,'available_models':[]}
    if _MODEL is not None and _MODEL_PATH==path and not force:
        return {'ok':True,'message':f'Model loaded: {path.name}','model':path.name,'available_models':[p.name for p in model_files()]}
    try:
        _,keras=lazy_tf(); _MODEL=keras.models.load_model(path, compile=False); _MODEL_PATH=path
        _MODEL.predict(np.zeros((1,IMAGE_SIZE[0],IMAGE_SIZE[1],3),dtype='float32'), verbose=0)
        return {'ok':True,'message':f'Model loaded: {path.name}','model':path.name,'available_models':[p.name for p in model_files()]}
    except Exception as exc:
        _MODEL=None; _MODEL_PATH=None
        return {'ok':False,'message':f'Model load failed: {exc}','model':None,'available_models':[p.name for p in model_files()]}
def model_status():
    return {**load_model(False),'image_size':IMAGE_SIZE,'expected_model_path':f"models/{CONFIG.get('model_filename','cantaloupe_model.keras')}"}
def read_image(raw:bytes):
    return ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert('RGB')
def crop_roi(img, mode, roi):
    iw,ih=img.size
    if mode!='roi': return img.copy(), {'x':0,'y':0,'w':iw,'h':ih}
    x=int(max(0,min(iw-1,roi.get('x',0)))); y=int(max(0,min(ih-1,roi.get('y',0))))
    w=int(max(8,min(iw-x,roi.get('w',iw)))); h=int(max(8,min(ih-y,roi.get('h',ih))))
    return img.crop((x,y,x+w,y+h)), {'x':x,'y':y,'w':w,'h':h}
def to_model_input(img): return img.resize(IMAGE_SIZE, Image.Resampling.BICUBIC).convert('RGB')
def batch_from_img(img224): return np.expand_dims(np.asarray(img224).astype('float32'),0)
def scalar_probability(raw):
    arr=np.asarray(raw,dtype='float32').reshape(-1)
    if arr.size==1: return float(np.clip(arr[0],0,1))
    vals=arr[:2]
    if np.any(vals<0) or not np.isclose(float(np.sum(vals)),1.0,atol=1e-2):
        exp=np.exp(vals-np.max(vals)); vals=exp/(np.sum(exp)+1e-8)
    return float(np.clip(vals[1],0,1))
def find_feature_layer(model):
    # top-level feature extractor layer first, best for saved Functional transfer-learning models
    for layer in reversed(model.layers):
        try:
            if len(layer.output.shape)==4: return layer.name, layer
        except Exception: pass
    return '', None
def jet_colormap(gray):
    x=np.clip(gray,0,1)
    r=np.clip(1.5-np.abs(4*x-3),0,1); g=np.clip(1.5-np.abs(4*x-2),0,1); b=np.clip(1.5-np.abs(4*x-1),0,1)
    return np.uint8(np.stack([r,g,b],axis=-1)*255)
def heat_to_images(heat,size):
    h=np.asarray(heat,dtype='float32').squeeze()
    if h.max()>h.min(): h=(h-h.min())/(h.max()-h.min()+1e-8)
    else: h=np.zeros_like(h)
    small=Image.fromarray(np.uint8(np.clip(h,0,1)*255),'L')
    block_gray=small.resize(size, Image.Resampling.NEAREST)
    smooth_gray=small.resize(size, Image.Resampling.BICUBIC)
    return Image.fromarray(jet_colormap(np.asarray(block_gray)/255.0),'RGB'), Image.fromarray(jet_colormap(np.asarray(smooth_gray)/255.0),'RGB')
def overlay_heatmap(base, heat, alpha=.45):
    base_arr=np.asarray(base.convert('RGB')).astype('float32'); heat_arr=np.asarray(heat.convert('RGB')).astype('float32')
    intensity=np.asarray(ImageOps.grayscale(heat)).astype('float32')/255.0
    mask=np.clip(.20+intensity[...,None]*.80,0,1)
    return Image.fromarray(np.uint8(np.clip(base_arr*(1-alpha*mask)+heat_arr*(alpha*mask),0,255)),'RGB')
def fallback_heatmap(base):
    gray=ImageEnhance.Contrast(ImageOps.grayscale(base).filter(ImageFilter.GaussianBlur(1))).enhance(2.2)
    arr=np.asarray(gray).astype('float32')/255.0; gy,gx=np.gradient(arr); sal=np.sqrt(gx*gx+gy*gy)
    if sal.max()>0: sal/=sal.max()
    return np.asarray(Image.fromarray(np.uint8(sal*255),'L').resize((7,7),Image.Resampling.BICUBIC)).astype('float32')/255.0
def compute_gradcam(batch, base224, prob, target):
    global _MODEL
    if _MODEL is None: raise RuntimeError('Model not loaded')
    try:
        tf,keras=lazy_tf(); lname,layer=find_feature_layer(_MODEL)
        if layer is None: raise RuntimeError('No connected 4D feature-map layer found.')
        grad_model=keras.models.Model(_MODEL.inputs,[layer.output,_MODEL.output])
        x=tf.convert_to_tensor(batch,dtype=tf.float32)
        with tf.GradientTape() as tape:
            conv,preds=grad_model(x,training=False); p=preds[:,0] if preds.shape[-1]==1 else preds[:,1]
            score = p if target=='cantaloupe' else (1.0-p if target=='not_cantaloupe' else (p if prob>=.5 else 1.0-p))
        grads=tape.gradient(score,conv)
        if grads is None: raise RuntimeError('Gradient was empty for selected feature map.')
        weights=tf.reduce_mean(grads,axis=(0,1,2)); cam=tf.reduce_sum(conv[0]*weights,axis=-1); cam=tf.nn.relu(cam).numpy()
        if (not np.isfinite(cam).all()) or cam.max()<=1e-8: raise RuntimeError('Grad-CAM returned an empty map.')
        block,smooth=heat_to_images(cam/(cam.max()+1e-8),base224.size)
        return block,smooth,'real_gradcam',lname,'Real Grad-CAM generated from the model feature map.'
    except Exception as exc:
        block,smooth=heat_to_images(fallback_heatmap(base224),base224.size)
        return block,smooth,'fallback_saliency','fallback',f'Prediction worked. Fallback saliency heatmap used because real Grad-CAM was unavailable: {exc}'
def make_study_panel(filename, out):
    cell=320; gap=42; top=86; bottom=48; w=cell*3+gap*4; h=top+cell+bottom
    canvas=Image.new('RGB',(w,h),'white'); draw=ImageDraw.Draw(canvas); font=ImageFont.load_default()
    imgs=[out.crop.resize((cell,cell)), out.heatmap_block.resize((cell,cell), Image.Resampling.NEAREST), out.overlay.resize((cell,cell))]
    titles=['Original','Grad-CAM Heatmap',f'Overlay\nPred: {out.predicted_label}\nP(cantaloupe)={out.probability_cantaloupe:.4f}']
    for i,(img,title) in enumerate(zip(imgs,titles)):
        x=gap+i*(cell+gap); y=top; canvas.paste(img,(x,y))
        for j,line in enumerate(title.split('\n')):
            bbox=draw.textbbox((0,0),line,font=font); draw.text((x+(cell-(bbox[2]-bbox[0]))/2,18+j*18),line,fill=(32,16,6),font=font)
    footer=f'{filename} | {out.gradcam_status} | layer: {out.gradcam_layer} | threshold={out.threshold:.2f}'
    draw.text((gap,h-28),footer[:160],fill=(95,55,18),font=font)
    return canvas
def predict(raw, filename, threshold, mode, roi, target):
    status=load_model(False)
    if not status.get('ok'): raise RuntimeError(status.get('message','Model not loaded.'))
    original=read_image(raw); crop, final_roi=crop_roi(original,mode,roi); base224=to_model_input(crop); batch=batch_from_img(base224)
    prob=scalar_probability(_MODEL.predict(batch,verbose=0)); threshold=float(np.clip(threshold,0,1))
    pos=CONFIG.get('positive_label','cantaloupe'); neg=CONFIG.get('negative_label','not_cantaloupe')
    pred=pos if prob>=threshold else neg; conf=prob if pred==pos else 1.0-prob
    heat_block, heat_smooth, status_gc, layer, note=compute_gradcam(batch,base224,prob,target); overlay=overlay_heatmap(base224,heat_smooth)
    temp=PredictionOutput(status.get('model') or 'model',pred,prob,1.0-prob,conf,threshold,status_gc,layer,note,base224,heat_block,heat_smooth,overlay,Image.new('RGB',(1,1)),final_roi)
    temp.study=make_study_panel(filename,temp)
    return temp
