@echo off
REM ============================================================================
REM The Code Master - System Starter Script
REM Starts required servers and initializes the Code Master system
REM Developed by Duncan N. for Developers
REM ============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Colors and formatting
echo.
echo ============================================================================
echo.
echo    _____ _            ___          _        __  ___           _            
echo   / ____^| ^|          / _ \        ^| ^|      /  ^^|/  ^^|         | ^|          
echo  ^| ^|    ^| ^|__   ___^| ^| ^| ^| _____ ^| ^| __ _  ^| ^|   ^^|   ___  ^| ^|_ ___  ___ ^|_^|
echo  ^| ^|    ^| '_ \ / _ \^| ^| ^| ^|/ _ \ \/ ^|/ _` ^| ^| ^|   ^| / _ \ / __ ^|/ _ \/ __^| '__^|
echo  ^| ^|____^| ^| ^| ^| (_) ^| ^|_^| ^| __/^>  <^| ^(_^| ^| ^| ^|__^| ^| (_) ^| ^| ^| ^| __/\__ \ ^| ^|  
echo   \____^|_^| ^|_^|\___/ \__,_^|\___^|_/\_\\__,_^| \_____\  \___/^|_^| ^|_^\___^||___/^|_^|  
echo.
echo   AI-Powered Code Documentation System
echo   Developed by Duncan N. for Developers
echo   © 2024-2025
echo.
echo ============================================================================
echo.

REM Check internet connection
echo [1/6] Checking internet connection...
ping -n 1 8.8.8.8 >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================================
    echo  ⚠️  No Internet Connection Detected
    echo ============================================================================
    echo.
    echo The Code Master requires internet connection for:
    echo   • GitHub repository access
    echo   • LLM integration (OpenAI API)
    echo   • Package downloads (if needed)
    echo.
    echo Please connect to the internet and try again.
    echo.
    set /p continue="Press any key to exit, or type 'continue' to proceed anyway: "
    if /i "!continue!" neq "continue" (
        echo.
        echo Exiting Code Master Starter...
        timeout /t 2 >nul
        exit /b 1
    )
    echo Proceeding without internet connection (offline mode enabled)...
    echo.
)

REM Check Python installation
echo [2/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================================
    echo  ❌ ERROR: Python is not installed or not in PATH
    echo ============================================================================
    echo.
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%A in ('python --version') do set PYTHON_VERSION=%%A
echo   ✅ Found %PYTHON_VERSION%

REM Check if virtual environment exists, if not create it
echo [3/6] Checking Python virtual environment...
if not exist "venv\" (
    echo   Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ============================================================================
        echo  ❌ ERROR: Failed to create virtual environment
        echo ============================================================================
        pause
        exit /b 1
    )
    echo   ✅ Virtual environment created
) else (
    echo   ✅ Virtual environment found
)

REM Activate virtual environment
echo [4/6] Installing required packages...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ============================================================================
    echo  ❌ ERROR: Failed to activate virtual environment
    echo ============================================================================
    pause
    exit /b 1
)
echo   ✅ Virtual environment activated

REM Install frontend dependencies
echo   Installing frontend dependencies...
cd CodebaseGenius\FE
if exist requirements.txt (
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt --quiet 2>nul
    if errorlevel 1 (
        echo   ⚠️  Warning: Some frontend packages may not have installed. Continuing...
    ) else (
        echo   ✅ Frontend dependencies installed
    )
) else (
    echo   ⚠️  Warning: FE requirements.txt not found
)
cd ..\..\

REM Install backend dependencies
echo   Installing backend dependencies...
cd CodebaseGenius\BE
if exist requirements.txt (
    python -m pip install -r requirements.txt --quiet 2>nul
    if errorlevel 1 (
        echo   ⚠️  Warning: Some backend packages may not have installed. Continuing...
    ) else (
        echo   ✅ Backend dependencies installed
    )
) else (
    echo   ⚠️  Warning: BE requirements.txt not found
)
cd ..\..\

REM Check required Python packages
echo [5/6] Verifying required packages...
python -c "import streamlit; print('   ✅ Streamlit found')" 2>nul || echo   ⚠️  Streamlit not found - installing...
python -c "import requests; print('   ✅ Requests found')" 2>nul || echo   ⚠️  Requests not found - installing...

REM Display system information
echo [6/6] System startup information...
echo.
echo   Environment Ready:
echo   • Python: %PYTHON_VERSION%
echo   • Virtual Environment: Activated
echo   • Frontend Port: 8502
echo   • Backend Port: 8001
echo.

REM Display startup instructions
echo ============================================================================
echo   STARTING THE CODE MASTER SYSTEM
echo ============================================================================
echo.
echo The system will start in the following order:
echo.
echo   1️⃣  Backend Server (JAC - Port 8001)
echo       • Multi-agent orchestration
echo       • REST API endpoints
echo       • Status: Ready (optional)
echo.
echo   2️⃣  Frontend Server (Streamlit - Port 8502)
echo       • Web interface
echo       • Real-time progress tracking
echo       • Status: Starting...
echo.
echo Once started, the frontend will open automatically at:
echo   🌐 http://localhost:8502
echo.
echo To use the system:
echo   1. Wait for the message: "Streamlit app is now running"
echo   2. A browser window should open automatically
echo   3. If not, manually open: http://localhost:8502
echo   4. Paste a GitHub URL in the "Generate Docs" tab
echo   5. Click validate and watch the progress!
echo.
echo To stop the system:
echo   1. Press Ctrl+C in this window
echo   2. If the browser doesn't close, close it manually
echo.
echo ============================================================================
echo.

REM Optional: Try to start backend (JAC server)
echo Starting backend services...
cd CodebaseGenius\BE

REM Check if JAC is available
python -c "import jac" >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  JAC not fully configured - Backend will run in demo mode
    echo   (Frontend will still work with demo documentation)
    echo.
) else (
    echo   ℹ️  Starting JAC backend server on port 8001 (in background)...
    REM Start JAC server in background (optional)
    REM Uncomment the line below if you want to auto-start JAC
    REM start "Code Master Backend" cmd /k "venv\Scripts\activate.bat && jac serve main.jac"
)

cd ..\..\

REM Start frontend server
echo.
echo ============================================================================
echo   STARTING STREAMLIT FRONTEND (Port 8502)
echo ============================================================================
echo.

cd CodebaseGenius\FE

REM -----------------------------------------------------------------------------
REM Start BSCN (B-Smart Career Navigator) backend + frontend if present
REM -----------------------------------------------------------------------------
if exist "BSCN\backend\app.py" (
    echo Starting BSCN backend on port 8002...
    start "BSCN Backend" cmd /k "cd /d %~dp0BSCN && venv_bscn\Scripts\activate.bat && python -m uvicorn backend.app:app --host 127.0.0.1 --port 8002"
) else (
    echo BSCN backend not found, skipping...
)

if exist "BSCN\frontend\streamlit_app.py" (
    echo Starting BSCN frontend on port 8502...
    start "BSCN Frontend" cmd /k "cd /d %~dp0BSCN && venv_bscn\Scripts\activate.bat && python -m streamlit run frontend\streamlit_app.py --server.port 8502"
) else (
    echo BSCN frontend not found, skipping...
)

REM Set environment variables for better performance
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

REM Start Streamlit
echo Launching Streamlit application...
echo.
python -m streamlit run code_master.py --server.port 8502 --client.showErrorDetails=true --logger.level=info

REM If we get here, the server stopped
echo.
echo ============================================================================
echo   SERVER STOPPED
echo ============================================================================
echo.
pause
exit /b 0
