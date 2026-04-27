from __future__ import annotations
import json, shutil, uuid
from pathlib import Path
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .settings import BASE_DIR, STATIC_DIR, TEMPLATE_DIR, MODELS_DIR, UPLOAD_DIR, RESULTS_DIR, CONFIG
from .database import init_db, insert, recent, stats, csv_export
from .ml import ALLOWED_IMAGE_EXTS, load_model, model_status, predict as run_prediction
app=FastAPI(title=CONFIG.get('app_name','CantaVision Grad-CAM Studio'), version='1.0.0')
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
app.mount('/data', StaticFiles(directory=BASE_DIR/'data'), name='data')
templates=Jinja2Templates(directory=TEMPLATE_DIR)
for d in [UPLOAD_DIR,RESULTS_DIR,MODELS_DIR]: d.mkdir(parents=True, exist_ok=True)
@app.on_event('startup')
def startup(): init_db(); load_model(False)
@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request':request,'config':CONFIG,'model_status':model_status(),'history':recent(12),'stats':stats()})
@app.get('/health')
def health(): return {'ok':True,'model':model_status(),'stats':stats()}
@app.post('/api/reload-model')
def reload_model(): return load_model(True)
@app.post('/api/upload-model')
async def upload_model(model_file: UploadFile=File(...)):
    suffix=Path(model_file.filename or '').suffix.lower()
    if suffix not in {'.keras','.h5','.hdf5'}: raise HTTPException(400,'Upload a .keras, .h5, or .hdf5 model file.')
    target=MODELS_DIR/str(CONFIG.get('model_filename','cantaloupe_model.keras')) if suffix=='.keras' else MODELS_DIR/f'uploaded_model{suffix}'
    with target.open('wb') as f: shutil.copyfileobj(model_file.file, f)
    return load_model(True)
@app.post('/api/predict')
async def api_predict(image: UploadFile=File(...), threshold: float=Form(.5), mode: str=Form('roi'), roi_json: str=Form('{}'), cam_target: str=Form('predicted')):
    suffix=Path(image.filename or 'image.jpg').suffix.lower() or '.jpg'
    if suffix not in ALLOWED_IMAGE_EXTS: raise HTTPException(400,'Upload JPG, PNG, WEBP, or BMP only.')
    raw=await image.read()
    if not raw: raise HTTPException(400,'No image uploaded.')
    if len(raw)>float(CONFIG.get('max_upload_mb',25))*1024*1024: raise HTTPException(413,'Image too large.')
    try: roi=json.loads(roi_json or '{}')
    except Exception: roi={}
    mode=mode if mode in {'roi','full'} else 'roi'; cam_target=cam_target if cam_target in {'predicted','cantaloupe','not_cantaloupe'} else 'predicted'
    stem=uuid.uuid4().hex; (UPLOAD_DIR/f'{stem}{suffix}').write_bytes(raw)
    try: out=run_prediction(raw, image.filename or f'{stem}{suffix}', threshold, mode, roi, cam_target)
    except Exception as exc: raise HTTPException(500,str(exc)) from exc
    crop_path=RESULTS_DIR/f'{stem}_crop.png'; heat_path=RESULTS_DIR/f'{stem}_heatmap_blocky.png'; smooth_path=RESULTS_DIR/f'{stem}_heatmap_smooth.png'; overlay_path=RESULTS_DIR/f'{stem}_overlay.png'; study_path=RESULTS_DIR/f'{stem}_study_panel.png'
    out.crop.save(crop_path); out.heatmap_block.save(heat_path); out.heatmap_smooth.save(smooth_path); out.overlay.save(overlay_path); out.study.save(study_path)
    row={'filename':image.filename or crop_path.name,'model_name':out.model_name,'mode':mode,'roi_x':out.roi['x'],'roi_y':out.roi['y'],'roi_w':out.roi['w'],'roi_h':out.roi['h'],'predicted_label':out.predicted_label,'probability_cantaloupe':out.probability_cantaloupe,'probability_not_cantaloupe':out.probability_not_cantaloupe,'confidence':out.confidence,'threshold':out.threshold,'gradcam_status':out.gradcam_status,'gradcam_layer':out.gradcam_layer,'crop_image':f'/data/results/{crop_path.name}','heatmap_image':f'/data/results/{heat_path.name}','smooth_heatmap_image':f'/data/results/{smooth_path.name}','overlay_image':f'/data/results/{overlay_path.name}','study_panel_image':f'/data/results/{study_path.name}'}
    pred_id=insert(row)
    return JSONResponse({'id':pred_id,**row,'note':out.note,'history':recent(12),'stats':stats()})
@app.get('/api/history')
def api_history(limit:int=18): return {'items':recent(limit),'stats':stats()}
@app.get('/api/history.csv')
def history_csv():
    return PlainTextResponse(csv_export(), media_type='text/csv', headers={'Content-Disposition':'attachment; filename=cantavision_prediction_history.csv'})
