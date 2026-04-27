# Hugging Face Deployment Guide

## Recommended Deployment Type

Use a **Hugging Face Space** with **Docker**.

## 1. Create the Space

1. Go to Hugging Face.
2. Click **New Space**.
3. Use this Space name:

```text
cantavision-gradcam-studio
```

4. Select **Docker** as the SDK.
5. Choose Public visibility if anyone should try it.

## 2. Upload the Project

Upload the complete project contents:

```text
app/
models/
docs/
Dockerfile
requirements.txt
README.md
config.json
```

## 3. Add the Model

Make sure the model exists at:

```text
models/cantaloupe_model.keras
```

## 4. Docker Port

The Dockerfile already runs:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

Hugging Face Spaces uses port `7860` by default for Docker Spaces.

## 5. Wait for Build

The first build can take several minutes because TensorFlow is large.

## 6. Test the Live Website

1. Open the public Space URL.
2. Upload an image.
3. Draw the ROI crop box.
4. Click **Predict ROI + Generate Grad-CAM**.
5. Confirm the heatmap, overlay, movable studio, and history database work.

## Troubleshooting

### Build is slow
TensorFlow is large, so the first build can take time.

### Space crashes from memory
Use only one final model file and consider upgrading Space hardware if needed.

### No model found
Confirm the file path is exactly:

```text
models/cantaloupe_model.keras
```
