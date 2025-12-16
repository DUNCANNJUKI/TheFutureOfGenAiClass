@echo off
chcp 65001 >nul
SETLOCAL
cd /d "%~dp0"










ENDLOCAL
:: donestart "B-Smart Backend" cmd /c "call venv\Scripts\activate.bat && python -m uvicorn backend.app:app --host 127.0.0.1 --port 8002"
:: start backend orchestrator (uvicorn)pip install -r backend\requirements.txtpython -m pip install --upgrade pipcall venv\Scripts\activate.batif not exist venv (python -m venv venv):: create venv if missing