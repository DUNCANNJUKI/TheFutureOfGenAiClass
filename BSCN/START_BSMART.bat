@echo off
rem START_BSMART.bat - starts BSCN backend and frontend and opens browser
setlocal
set ROOT_DIR=%~dp0
rem Activate backend venv and start uvicorn in a new window
start "BSCN Backend" cmd /k "cd /d "%ROOT_DIR%" && if exist venv_bscn\Scripts\activate.bat (call venv_bscn\Scripts\activate.bat) else (echo Warning: venv_bscn not found) && python -m uvicorn backend.app:app --host 127.0.0.1 --port 8002"
rem Start Streamlit frontend in a new window
start "BSCN Frontend" cmd /k "cd /d "%ROOT_DIR%" && if exist venv_bscn\Scripts\activate.bat (call venv_bscn\Scripts\activate.bat) && python -m streamlit run frontend\streamlit_app.py --server.port 8502"
rem Wait briefly then open browser
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8502"
endlocal
@echo off
chcp 65001 >nul
SETLOCAL
cd /d "%~dp0"










ENDLOCAL
:: donestart "B-Smart Backend" cmd /c "call venv\Scripts\activate.bat && python -m uvicorn backend.app:app --host 127.0.0.1 --port 8002"
:: start backend orchestrator (uvicorn)pip install -r backend\requirements.txtpython -m pip install --upgrade pipcall venv\Scripts\activate.batif not exist venv (python -m venv venv):: create venv if missing