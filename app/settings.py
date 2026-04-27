from pathlib import Path
import json
BASE_DIR = Path(__file__).resolve().parents[1]
APP_DIR = BASE_DIR / "app"
STATIC_DIR = APP_DIR / "static"
TEMPLATE_DIR = APP_DIR / "templates"
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
RESULTS_DIR = DATA_DIR / "results"
DB_DIR = DATA_DIR / "db"
CONFIG_PATH = BASE_DIR / "config.json"
DEFAULT_CONFIG = {
    "app_name": "CantaVision Grad-CAM Studio",
    "academic_title": "CantaVision Grad-CAM Studio: A Web-Deployed Cantaloupe Classification System Using Transfer Learning, Region-of-Interest Cropping, and Interactive Model Explainability",
    "student_name": "Tristan Job Ulita",
    "school": "National University - Lipa | School of Architecture, Computing, and Engineering | BS Computer Science",
    "model_filename": "cantaloupe_model.keras",
    "image_size": [224, 224],
    "positive_label": "cantaloupe",
    "negative_label": "not_cantaloupe",
    "default_threshold": 0.50,
    "max_upload_mb": 25,
    "preprocessing_note": "Selected ROI is resized to 224x224 and converted to float32 before prediction."
}
def load_config() -> dict:
    cfg = DEFAULT_CONFIG.copy()
    if CONFIG_PATH.exists():
        try:
            cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
        except Exception:
            pass
    return cfg
CONFIG = load_config()
IMAGE_SIZE = tuple(int(x) for x in CONFIG.get("image_size", [224,224]))
