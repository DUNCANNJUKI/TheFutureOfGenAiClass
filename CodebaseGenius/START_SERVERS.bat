@echo off
REM Start Codebase Genius System
REM This script starts both the JAC backend and Streamlit frontend

echo.
echo ===================================================
echo Codebase Genius - System Startup
echo ===================================================
echo.
echo Starting backend and frontend servers...
echo.

REM Get the current directory
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

REM Start backend JAC server
echo [1/2] Starting JAC Backend Server on port 8000...
echo.
start "Codebase Genius Backend" cmd /k "cd BE && venv\Scripts\activate.bat && jac serve main.jac"

REM Wait a few seconds for backend to start
timeout /t 5 /nobreak

REM Start frontend Streamlit
echo.
echo [2/2] Starting Streamlit Frontend on port 8501...
echo.
start "Codebase Genius Frontend" cmd /k "cd FE && python -m streamlit run app.py --logger.level=info"

echo.
echo ===================================================
echo System Startup Complete!
echo ===================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8501
echo.
echo Close these windows to stop the servers.
echo Streamlit will open automatically in your browser.
echo.
pause
