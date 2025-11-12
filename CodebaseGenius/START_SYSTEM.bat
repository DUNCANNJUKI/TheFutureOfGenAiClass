@echo off
REM Code Master System Startup Script
REM Starts both backend (port 8001) and frontend (port 8502)

echo.
echo ========================================
echo     CODE MASTER - SYSTEM STARTUP
echo ========================================
echo.

REM Get the directory where this script is located
setlocal enabledelayedexpansion
set SCRIPT_DIR=%~dp0
set BE_DIR=%SCRIPT_DIR%CodebaseGenius\BE
set FE_DIR=%SCRIPT_DIR%CodebaseGenius\FE

REM Check if virtual environment exists
if not exist "%BE_DIR%\venv" (
    echo [ERROR] Virtual environment not found at %BE_DIR%\venv
    echo Please run: python -m venv %BE_DIR%\venv
    pause
    exit /b 1
)

echo [INFO] Backend directory: %BE_DIR%
echo [INFO] Frontend directory: %FE_DIR%
echo.

REM Start backend in a new window
echo [INFO] Starting backend server on port 8001...
start "Code Master Backend" cmd /k "cd %BE_DIR% && %BE_DIR%\venv\Scripts\python.exe -m uvicorn server:app --host 0.0.0.0 --port 8001"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start frontend in a new window
echo [INFO] Starting frontend on port 8502...
start "Code Master Frontend" cmd /k "cd %FE_DIR% && %BE_DIR%\venv\Scripts\streamlit.exe run code_master.py --server.port 8502"

echo.
echo ========================================
echo     SYSTEM STARTED SUCCESSFULLY
echo ========================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:8502
echo API Docs: http://localhost:8001/docs
echo.
echo Press any key to continue...
pause
