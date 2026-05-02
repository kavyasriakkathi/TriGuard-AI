@echo off
setlocal
title TriGuard AI - Dashboard Launcher

echo ===================================================
echo 🛡️  TriGuard AI - Dashboard Launcher
echo ===================================================
echo.

:: Check for virtual environment
set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo 📦 Using virtual environment (.venv)
)

:: Check if Python is installed
%PYTHON_EXE% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in your PATH.
    echo Please install Python 3.10+ and try again.
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
%PYTHON_EXE% -m pip install streamlit pandas plotly scikit-learn rich --quiet
if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to install dependencies.
    pause
    exit /b %errorlevel%
)
echo ✅ Dependencies confirmed.
echo.

echo [2/3] Starting the Streamlit Web Server...
echo ⚠️  IMPORTANT: Keep this window open!
echo Closing this window will stop the TriGuard AI dashboard.
echo.
echo The app will open at: http://localhost:8501
echo.

:: Try to start streamlit
%PYTHON_EXE% -m streamlit run app.py --server.port 8501 --server.headless false
if %errorlevel% neq 0 (
    echo ⚠️  '%PYTHON_EXE% -m streamlit' failed. Trying direct 'streamlit run'...
    streamlit run app.py --server.port 8501 --server.headless false
)

if %errorlevel% neq 0 (
    echo ❌ FATAL ERROR: Streamlit failed to start.
    echo Check if another application is using port 8501.
)

echo.
echo Dashboard stopped.
pause

