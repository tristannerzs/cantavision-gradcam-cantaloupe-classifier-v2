# Sir Joel Run Instructions

## Project Title

**CantaVision Grad-CAM Studio: A Web-Deployed Cantaloupe Classification System Using Transfer Learning, Region-of-Interest Cropping, and Interactive Model Explainability**

## Project Description

I made this website as the deployment component of my binary cantaloupe image classification project. The web application allows a user to upload an image, select a specific region of interest, classify the selected crop as **cantaloupe** or **not_cantaloupe**, and inspect the prediction using a Grad-CAM heatmap similar to the heatmap figures from my notebook output.

## Required Model File

Place the trained model in this exact location:

```text
models/cantaloupe_model.keras
```

Recommended model file:

```text
MIDTERM_Tristan_Job_Ulita_Model2_EfficientNetB0.keras
```

Rename it to:

```text
cantaloupe_model.keras
```

## Windows Run Instructions

1. Extract the project ZIP.
2. Open the extracted folder.
3. Copy the trained model into `models/cantaloupe_model.keras`.
4. Double-click `launch_windows.bat`.
5. Wait for the dependencies to install.
6. Open `http://127.0.0.1:8000`.

## Manual VS Code Run Instructions

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Test Checklist

1. Upload an image.
2. Move the orange crop box around one specific fruit or leaf area.
3. Click **Predict ROI + Generate Grad-CAM**.
4. Confirm these panels appear:
   - Original ROI / Model Input
   - Grad-CAM Heatmap
   - Overlay
   - Notebook-style study panel
   - Movable heatmap studio
5. Drag the heatmap in the studio.
6. Adjust opacity, scale, X/Y movement, and crop mask.
7. Export the prediction CSV.

## Demo Mode

The website has a demo button so the interface can be reviewed before adding the model. Real prediction requires the `.keras` model.
