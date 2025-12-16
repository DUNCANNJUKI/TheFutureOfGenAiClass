@echo off
chcp 65001 >nul
SETLOCAL
set ROOT=%~dp0
cd /d "%ROOT%"

if not exist venv (python -m venv venv)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

start "backend" cmd /c "call venv\Scripts\activate.bat && python -m uvicorn backend.app:app --host 127.0.0.1 --port 8001"
start "frontend" cmd /c "call venv\Scripts\activate.bat && python -m streamlit run frontend\streamlit_app.py --server.port 8502"
ENDLOCAL
