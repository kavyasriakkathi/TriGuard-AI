@echo off
setlocal
title TriGuard AI - System Diagnostics

echo ===================================================
echo 🔍 TriGuard AI: SYSTEM DIAGNOSTICS
echo ===================================================
echo.

:: 1. Check Python
echo [STEP 1] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not found in your PATH.
    echo Please install Python from python.org
    goto :end
)
python --version
echo ✅ Python is OK.
echo.

:: 2. Check Virtual Environment
echo [STEP 2] Checking Virtual Environment...
if exist ".venv\Scripts\python.exe" (
    echo ✅ .venv found.
    set "PY=.venv\Scripts\python.exe"
) else (
    echo ⚠️  .venv not found. Using global Python.
    set "PY=python"
)
echo.

:: 3. Check Streamlit Installation
echo [STEP 3] Checking Streamlit...
%PY% -m streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Streamlit is NOT installed in this environment.
    echo 🛠️  Attempting to install now...
    %PY% -m pip install streamlit pandas plotly scikit-learn rich
)
%PY% -m streamlit --version
echo ✅ Streamlit is OK.
echo.

:: 4. Check for Port Conflicts
echo [STEP 4] Checking if Port 8501 is busy...
netstat -aon | findstr :8501 | findstr LISTENING
if %errorlevel% equ 0 (
    echo ⚠️  Port 8501 is ALREADY in use by another program.
    echo 🔪 Attempting to clear it...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
) else (
    echo ✅ Port 8501 is free.
)
echo.

:: 5. Deep Import Test (Checking app.py dependencies)
echo [STEP 5] Checking all app dependencies...
%PY% -c "import streamlit, pandas, plotly, sklearn, rich; print('✅ All libraries found')"
if %errorlevel% neq 0 (
    echo ❌ ERROR: One or more libraries are missing or broken.
    echo Attempting to fix...
    %PY% -m pip install -r requirements.txt
)

echo [STEP 6] Checking for code syntax errors in app.py...
%PY% -m py_compile app.py
if %errorlevel% neq 0 (
    echo ❌ ERROR: app.py has a syntax error! 
    pause
    exit /b
)
echo ✅ app.py is valid.
echo.

echo ===================================================
echo 🚀 ALL SYSTEMS CLEAR. Starting Dashboard...
echo ===================================================
echo Command: %PY% -m streamlit run app.py --server.port 8502
%PY% -m streamlit run app.py --server.port 8502 --server.address 127.0.0.1
if %errorlevel% neq 0 (
    echo.
    echo ❌ THE SERVER CRASHED. 
    echo Look at the RED TEXT above and tell me what it says!
)

:end
echo.
pause
