@echo off
echo ===================================================
echo 🚀 TriGuard AI - Dashboard Launcher
echo ===================================================
echo.

echo [1/3] Checking dependencies...
python -m pip install streamlit pandas plotly scikit-learn rich --quiet
if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to install dependencies. Please check your internet connection and ensure Python is in your PATH.
    pause
    exit /b %errorlevel%
)
echo ✅ Dependencies confirmed.
echo.

echo [2/3] Starting the Streamlit Web Server...
echo ⚠️ PLEASE LEAVE THIS WINDOW OPEN DURING YOUR DEMO!
echo.
echo The app will open at: http://localhost:8501
echo.

python -m streamlit run app.py --server.port 8501
if %errorlevel% neq 0 (
    echo ⚠️ 'python -m streamlit' failed. Trying direct 'streamlit run'...
    streamlit run app.py --server.port 8501
)

if %errorlevel% neq 0 (
    echo ❌ FATAL ERROR: Streamlit failed to start.
    echo Please copy the error message above and paste it here so I can fix it for you!
)

pause
