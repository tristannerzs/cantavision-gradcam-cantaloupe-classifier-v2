---
title: CantaVision Grad-CAM Studio v2
emoji: 🍈
colorFrom: orange
colorTo: yellow
sdk: docker
app_port: 7860
---

# CantaVision Grad-CAM Studio v2

**Project Title:** CantaVision Grad-CAM Studio v2: A Web-Deployed Cantaloupe Classification System Using Transfer Learning, Region-of-Interest Cropping, and Interactive Model Explainability

This is the complete web deployment package I made for my binary cantaloupe image classification project. It turns my saved TensorFlow/Keras model into an interactive website with ROI cropping, threshold control, Grad-CAM explainability, SQLite prediction history, CSV export, GitHub-ready files, and Hugging Face Docker deployment.

## What I Made

I made a complete FastAPI web application where users can upload an image, draw a crop box around one specific fruit or leaf area, run classification on that selected ROI, and inspect the result using a Grad-CAM heatmap. The heatmap is styled like the notebook screenshots: blocky, high-contrast, and jet-colored. The app also includes a separate movable Grad-CAM studio where the heatmap can be dragged, resized, masked, and studied interactively.

## Main Features

- Modern orange/white retro game-style interface
- Cute replaceable pixel NPC and animated falling fruit particles
- Image upload with mobile camera support
- Interactive ROI crop box with drag and resize handles
- Full-image mode and ROI-crop mode
- Adjustable confidence threshold
- Real Keras model prediction using `models/cantaloupe_model.keras`
- Grad-CAM heatmap generation from the saved model feature map
- Blocky jet-style heatmap matching the notebook visual style
- Smooth overlay heatmap
- Notebook-style study panel: Original, Grad-CAM Heatmap, Overlay
- Movable Grad-CAM studio with drag, resize, opacity, scale, X/Y, crop mask, and grid controls
- SQLite prediction database
- CSV export
- Model reload button
- Optional local model upload
- Demo mode for UI preview
- Windows launcher
- Mac/Linux launcher
- Dockerfile for Hugging Face Spaces
- Render deployment configuration
- GitHub Actions syntax check

## Required Model Location

Copy your best trained model here:

```text
models/cantaloupe_model.keras
```

Recommended model:

```text
MIDTERM_Tristan_Job_Ulita_Model2_EfficientNetB0.keras
```

Rename it exactly:

```text
cantaloupe_model.keras
```

## Local Run on Windows

Double-click:

```text
launch_windows.bat
```

Then open:

```text
http://127.0.0.1:8000
```

## Manual VS Code Run

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Local Run on Mac/Linux

```bash
chmod +x launch_macos_linux.sh
./launch_macos_linux.sh
```

Open:

```text
http://127.0.0.1:8000
```

## How to Use the Website

1. Open the website.
2. Upload a cantaloupe or non-cantaloupe image.
3. If the image has multiple fruits, choose ROI crop mode.
4. Drag the orange ROI box around the exact fruit or leaf area.
5. Click **Predict ROI + Generate Grad-CAM**.
6. View the Original ROI, Grad-CAM Heatmap, and Overlay panels.
7. Open the notebook-style study panel image.
8. Use the movable heatmap studio to drag, scale, mask, and analyze the heatmap.
9. Export prediction history using the CSV button.

## Prediction Logic

The website uses:

```text
P(cantaloupe) >= threshold  -> cantaloupe
P(cantaloupe) < threshold   -> not_cantaloupe
```

The selected ROI is resized to `224 x 224` before prediction.

## Important Instruction Files

```text
docs/PROFESSOR_RUN_INSTRUCTIONS.md
docs/GITHUB_UPLOAD_GUIDE.md
docs/HUGGINGFACE_DEPLOYMENT_GUIDE.md
docs/FULL_STEP_BY_STEP_GITHUB_AND_HUGGINGFACE.md
docs/ACADEMIC_PROJECT_TITLES.md
docs/STUDENT_PRESENTATION_SCRIPT.md
docs/FINAL_SUBMISSION_README_FOR_PROFESSOR.md
```

## Customization

Replace these files if you want new art:

```text
app/static/assets/npc.svg
app/static/assets/cantaloupe.svg
app/static/assets/placeholder-wide.svg
```

Change design colors and effects in:

```text
app/static/css/style.css
```
