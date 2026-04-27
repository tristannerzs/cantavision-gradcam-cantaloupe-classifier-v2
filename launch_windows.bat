@echo off
setlocal
cd /d "%~dp0"
echo ==========================================================
echo CantaVision Grad-CAM Studio - Windows Local Launcher
echo ==========================================================
if not exist .venv (
  echo Creating Python virtual environment...
  py -3.11 -m venv .venv || py -3.10 -m venv .venv || python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist models\cantaloupe_model.keras (
  echo.
  echo WARNING: models\cantaloupe_model.keras was not found.
  echo Put your trained .keras model in the models folder before real prediction.
  echo The website demo mode will still work.
  echo.
)
echo Opening at http://127.0.0.1:8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
