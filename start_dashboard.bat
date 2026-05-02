@echo off
setlocal
title TriGuard AI - Premium Dashboard Launcher

echo ===================================================
echo 🛡️  TriGuard AI - Dashboard Launcher
echo ===================================================
echo.

:: 1. Cleanup: Kill any existing processes on port 8501
echo 🔍 Checking for existing dashboard processes on port 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING') do (
    if not "%%a"=="" (
        echo 🔪 Closing ghost process (PID: %%a) to resolve port conflict...
        taskkill /F /PID %%a >nul 2>&1
    )
)

:: 2. Environment Setup
set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo 📦 Using virtual environment (.venv)
) else (
    echo 🌐 Using global Python system
)

:: 3. Dependencies Check
echo [1/2] Verifying core dependencies...
%PYTHON_EXE% -c "import streamlit, pandas, plotly, sklearn, rich" >nul 2>&1
if %errorlevel% neq 0 (
    echo 🛠️  Installing missing dependencies from requirements.txt...
    %PYTHON_EXE% -m pip install -r requirements.txt --quiet
) else (
    echo ✅ Dependencies verified.
)

:: 4. Start Streamlit
echo [2/2] Starting the Streamlit Web Server...
echo ⚠️  IMPORTANT: Keep this window open!
echo.

:: We use --server.headless false to ensure it opens the browser
:: We use --browser.gatherUsageStats false for privacy and speed
%PYTHON_EXE% -m streamlit run app.py --server.port 8505 --server.address 127.0.0.1 --server.headless false --browser.gatherUsageStats false

if %errorlevel% neq 0 (
    echo.
    echo ❌ FATAL ERROR: Streamlit failed to start.
    echo ---------------------------------------------------
    echo Troubleshooting:
    echo 1. Check if port 8501 is blocked by a firewall.
    echo 2. Run 'pip install -r requirements.txt' manually.
    echo 3. Ensure app.py is in the current directory.
    echo ---------------------------------------------------
)

echo.
echo Dashboard stopped.
pause

