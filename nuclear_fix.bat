@echo off
setlocal
title TriGuard AI - NUCLEAR RECOVERY

echo ===================================================
echo 🔥 TriGuard AI: NUCLEAR RECOVERY ENGINE
echo ===================================================
echo.

:: 1. Clear all Python processes
echo 🧹 Cleaning up Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM streamlit.exe /T >nul 2>&1
echo ✅ Cleanup complete.

:: 2. Delete and Rebuild Virtual Environment
echo 🏗️  Rebuilding Python environment (this takes a minute)...
if exist ".venv" (
    echo 🗑️  Removing broken environment...
    rmdir /s /q .venv
)
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ FAILED to create virtual environment. Ensure Python is installed.
    pause
    exit /b
)
echo ✅ Environment rebuilt.

:: 3. Force Re-install Dependencies
echo 🛠️  Installing fresh libraries...
.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.venv\Scripts\python.exe -m pip install streamlit pandas plotly scikit-learn rich --quiet
echo ✅ Dependencies re-installed.

:: 4. Verify app.py
echo 🔬 Running code integrity check...
.venv\Scripts\python.exe -m py_compile app.py
if %errorlevel% neq 0 (
    echo ❌ CRITICAL: Your app.py has a syntax error!
    pause
    exit /b
)
echo ✅ app.py is healthy.

:: 5. Launch with absolute settings
echo 🚀 Launching on Port 8505...
.venv\Scripts\python.exe -m streamlit run app.py --server.port 8505 --server.address 127.0.0.1 --server.headless false

if %errorlevel% neq 0 (
    echo.
    echo ❌ FAILED TO START. 
    echo Please copy any RED TEXT you see above and send it to me!
)

pause
