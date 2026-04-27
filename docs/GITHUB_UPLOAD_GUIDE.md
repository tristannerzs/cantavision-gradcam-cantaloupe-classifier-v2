# GitHub Upload Guide

## 1. Prepare the Folder

Make sure the folder contains:

```text
app/
models/
data/
docs/
Dockerfile
requirements.txt
README.md
launch_windows.bat
config.json
```

## 2. Add the Model

Copy the model into:

```text
models/cantaloupe_model.keras
```

If the model is too large, use Git LFS or upload the model directly to Hugging Face.

## 3. Create the GitHub Repository

Recommended repository name:

```text
cantavision-gradcam-cantaloupe-classifier
```

## 4. Push with Git

```bash
git init
git add .
git commit -m "Initial CantaVision Grad-CAM Studio website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cantavision-gradcam-cantaloupe-classifier.git
git push -u origin main
```

## 5. If the Model Is Large, Use Git LFS

```bash
git lfs install
git lfs track "*.keras"
git add .gitattributes models/cantaloupe_model.keras
git commit -m "Add trained cantaloupe model with Git LFS"
git push
```

## Suggested Repository Description

```text
A web-deployed binary cantaloupe image classifier with ROI cropping, confidence thresholding, SQLite prediction logging, and interactive Grad-CAM heatmap visualization.
```
