@echo off
REM ============================================================================
REM Code Master v2.0 - Complete System Startup
REM One-click launcher for Backend + Frontend + Browser
REM Developed by Duncan N. for Developers (2024-2026)
REM ============================================================================

setlocal enabledelayedexpansion
title Code Master v2.0 - System Launcher
color 0A

REM Get script directory
set SCRIPT_DIR=%~dp0
set BE_DIR=%SCRIPT_DIR%CodebaseGenius\BE
set FE_DIR=%SCRIPT_DIR%CodebaseGenius\FE

REM ============================================================================
REM WELCOME BANNER
REM ============================================================================

cls
echo.
echo   ╔═══════════════════════════════════════════════════════════════╗
echo   ║                                                               ║
echo   ║            CODE MASTER v2.0 - SYSTEM LAUNCHER                ║
echo   ║                                                               ║
echo   ║  Multi-Agent AI Documentation Generation Platform            ║
echo   ║  Developed by Duncan N. for Developers (2024-2026)           ║
echo   ║                                                               ║
echo   ╚═══════════════════════════════════════════════════════════════╝
echo.
timeout /t 1 /nobreak

REM ============================================================================
REM CHECKS
REM ============================================================================

echo [*] Performing system checks...

REM Check if virtual environment exists
if not exist "%BE_DIR%\venv" (
    echo [ERROR] Virtual environment not found!
    echo [INFO] Creating virtual environment...
    python -m venv "%BE_DIR%\venv"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo [INFO] Make sure Python 3.10+ is installed
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Check if Python is available
"%BE_DIR%\venv\Scripts\python.exe" --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in virtual environment
    pause
    exit /b 1
)
echo [OK] Python environment ready

REM Check if required packages are installed
"%BE_DIR%\venv\Scripts\python.exe" -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required packages...
    "%BE_DIR%\venv\Scripts\pip.exe" install -q fastapi uvicorn requests streamlit
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

echo.
echo ============================================================
echo                  STARTING SERVICES
echo ============================================================
echo.

REM ============================================================================
REM START BACKEND
REM ============================================================================

echo [*] Starting Backend Server (Port 8001)...
start "Code Master - Backend (Port 8001)" cmd /k "cd "%BE_DIR%" && "%BE_DIR%\venv\Scripts\python.exe" -m uvicorn server_v2:app --host 0.0.0.0 --port 8001 --reload"

REM Wait for backend to start
echo [*] Waiting for backend to initialize...
timeout /t 3 /nobreak

REM ============================================================================
REM START FRONTEND
REM ============================================================================

echo [*] Starting Frontend Application (Port 8502)...
start "Code Master - Frontend (Port 8502)" cmd /k "cd "%FE_DIR%" && "%BE_DIR%\venv\Scripts\streamlit.exe" run code_master_v2.py --server.port 8502 --logger.level=warning"

REM Wait for frontend to start
echo [*] Waiting for frontend to initialize...
timeout /t 4 /nobreak

REM ============================================================================
REM OPEN BROWSER
REM ============================================================================

echo [*] Opening browser...
timeout /t 1 /nobreak
start "" http://localhost:8502

REM ============================================================================
REM SUCCESS MESSAGE
REM ============================================================================

cls
echo.
echo   ╔═══════════════════════════════════════════════════════════════╗
echo   ║                                                               ║
echo   ║              SYSTEM STARTED SUCCESSFULLY!                    ║
echo   ║                                                               ║
echo   ║  Version: 2.0.0                                              ║
echo   ║  Status: All services running                                ║
echo   ║                                                               ║
echo   ╠═══════════════════════════════════════════════════════════════╣
echo   ║  SERVICES RUNNING                                             ║
echo   ╠═══════════════════════════════════════════════════════════════╣
echo   ║                                                               ║
echo   ║  Frontend   : http://localhost:8502                           ║
echo   ║  Backend    : http://localhost:8001                           ║
echo   ║  API Docs   : http://localhost:8001/docs                      ║
echo   ║  Health     : http://localhost:8001/health                    ║
echo   ║                                                               ║
echo   ╠═══════════════════════════════════════════════════════════════╣
echo   ║  FEATURES AVAILABLE                                           ║
echo   ╠═══════════════════════════════════════════════════════════════╣
echo   ║                                                               ║
echo   ║  + Multi-Agent AI Analysis                                    ║
echo   ║  + Smart Chatbot Q&A                                          ║
echo   ║  + API Endpoint Extraction                                    ║
echo   ║  + Documentation Export (MD/HTML/JSON/TXT)                    ║
echo   ║  + Real-time Processing                                       ║
echo   ║  + Professional Output                                        ║
echo   ║                                                               ║
echo   ╠═══════════════════════════════════════════════════════════════╣
echo   ║  TROUBLESHOOTING                                              ║
echo   ╠═══════════════════════════════════════════════════════════════╣
echo   ║                                                               ║
echo   ║  - Backend not running?                                       ║
echo   ║    Check window titled "Code Master - Backend"                ║
echo   ║                                                               ║
echo   ║  - Frontend not loading?                                      ║
echo   ║    Check window titled "Code Master - Frontend"               ║
echo   ║                                                               ║
echo   ║  - Browser didn't open?                                       ║
echo   ║    Manually visit http://localhost:8502                       ║
echo   ║                                                               ║
echo   ╠═══════════════════════════════════════════════════════════════╣
echo   ║  DEVELOPED BY: Duncan N. for Developers (2024-2026)           ║
echo   ║                                                               ║
echo   ╚═══════════════════════════════════════════════════════════════╝
echo.
echo Press any key to keep this window open, or close it to stop services.
pause

REM ============================================================================
REM END
REM ============================================================================

exit /b 0
