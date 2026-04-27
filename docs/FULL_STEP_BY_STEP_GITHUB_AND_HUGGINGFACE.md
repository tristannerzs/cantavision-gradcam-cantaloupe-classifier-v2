# Full Step-by-Step: Upload to GitHub and Deploy to Hugging Face

This is the complete deployment instruction file I would submit with the project so the website can be uploaded to GitHub and deployed as a public Hugging Face website.

## Final Project Title

**CantaVision Grad-CAM Studio: A Web-Deployed Cantaloupe Classification System Using Transfer Learning, Region-of-Interest Cropping, and Interactive Model Explainability**

---

# Part 1 - Run Locally Before Uploading

## 1. Extract the ZIP

Extract the folder named:

```text
CantaVision_GradCAM_Studio_FINAL
```

## 2. Add the Trained Model

Copy the best trained Keras model into:

```text
models/cantaloupe_model.keras
```

The model filename must be exactly:

```text
cantaloupe_model.keras
```

## 3. Run Locally

On Windows, double-click:

```text
launch_windows.bat
```

Or run manually:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 4. Test Before Upload

- Upload a fruit image.
- Move the ROI crop box.
- Predict.
- Confirm Grad-CAM heatmap appears.
- Move the heatmap in the studio.
- Export CSV.

---

# Part 2 - Upload to GitHub

## 1. Create a Repository

Create a new GitHub repository named:

```text
cantavision-gradcam-cantaloupe-classifier
```

## 2. Open Terminal in the Project Folder

Make sure you are inside the folder that contains:

```text
app/
Dockerfile
README.md
requirements.txt
```

## 3. Initialize Git and Push

```bash
git init
git add .
git commit -m "Initial CantaVision Grad-CAM Studio website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cantavision-gradcam-cantaloupe-classifier.git
git push -u origin main
```

## 4. If the Model Is Too Large

Use Git LFS:

```bash
git lfs install
git lfs track "*.keras"
git add .gitattributes models/cantaloupe_model.keras
git commit -m "Add trained cantaloupe model with Git LFS"
git push
```

---

# Part 3 - Deploy to Hugging Face Spaces

## 1. Create a Hugging Face Space

- Go to Hugging Face.
- Create a new Space.
- Space name:

```text
cantavision-gradcam-studio
```

- SDK: **Docker**
- Visibility: Public

## 2. Upload Files

Upload the same project files from GitHub or push them through Git.

Required files:

```text
app/
models/cantaloupe_model.keras
Dockerfile
requirements.txt
README.md
config.json
```

## 3. Confirm the Dockerfile

The included Dockerfile exposes and runs the app on port 7860:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

## 4. Wait for Build

Hugging Face will build the Docker container. TensorFlow can take several minutes to install.

## 5. Test the Public Website

Open the Space URL and test:

- Upload image
- ROI crop
- Prediction
- Grad-CAM heatmap
- Notebook-style study panel
- Movable heatmap studio
- CSV export

---

# Part 4 - What to Submit

Submit these links:

```text
GitHub Repository: https://github.com/YOUR_USERNAME/cantavision-gradcam-cantaloupe-classifier
Hugging Face Space: https://huggingface.co/spaces/YOUR_USERNAME/cantavision-gradcam-studio
```

Also submit this explanation:

> I made CantaVision Grad-CAM Studio as a web-deployed binary cantaloupe classification system. It uses my trained TensorFlow/Keras model, allows ROI cropping for specific fruit selection, applies threshold-based prediction, generates Grad-CAM heatmaps for explainability, saves predictions in SQLite, and includes a movable heatmap studio for interactive model interpretation.
