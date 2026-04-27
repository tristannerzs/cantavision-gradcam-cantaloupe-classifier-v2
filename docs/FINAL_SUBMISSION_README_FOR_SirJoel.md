# Final Submission Summary for Sir Joel

## Project Title

**CantaVision Grad-CAM Studio: A Web-Deployed Cantaloupe Classification System Using Transfer Learning, Region-of-Interest Cropping, and Interactive Model Explainability**

## What I Made

I made a complete web application for my cantaloupe classification project. It deploys my trained TensorFlow/Keras model and allows users to classify fruit images through a browser interface. The website also includes Grad-CAM explainability so the prediction can be visually interpreted.

## Main Components

- Transfer learning model deployment
- Binary classification between cantaloupe and not_cantaloupe
- Region-of-interest image selection
- Confidence threshold adjustment
- Grad-CAM visual interpretability
- SQLite-based prediction history
- CSV export for traceability
- GitHub-ready and Hugging Face-ready deployment structure

## How It Connects to My Training Work

The training project compared MobileNetV2 and EfficientNetB0 using the same two-stage training setup. The best model from the comparison can be placed into the website as `models/cantaloupe_model.keras`. The web application then uses that saved model for real inference.

## What to Run

On Windows:

```text
launch_windows.bat
```

Then open:

```text
http://127.0.0.1:8000
```

## Required Model Location

```text
models/cantaloupe_model.keras
```

## Final Notes

The website includes a demo mode so the interface can still be previewed even before the model is added. Real prediction and Grad-CAM require the trained Keras model file.
