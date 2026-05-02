@echo off
setlocal
title TriGuard AI - GitHub Sync Engine

echo ===================================================
echo 🛡️  TriGuard AI - GitHub Sync Engine
echo ===================================================
echo.

:: 1. Verify Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Git is not installed.
    pause
    exit /b 1
)

:: 2. Initialize if needed
if not exist ".git" (
    echo 🏗️  Initializing new Git repository...
    git init
    git branch -M main
)

:: 3. Set Remote (Force update to kavyasriakkathi/TriGuard-AI)
echo 🔗 Configuring remote origin...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/kavyasriakkathi/TriGuard-AI.git

:: 4. Stage and Commit
echo 📦 Staging all files...
git add .

:: Filter out large/unnecessary files if they exist
git reset -- logs.json >nul 2>&1
git reset -- output.csv >nul 2>&1
git reset -- triguard_model.pkl >nul 2>&1

set "msg=Sync: TriGuard AI Premium Update %date% %time%"
echo 📝 Committing with message: "%msg%"
git commit -m "%msg%"

:: 5. Push
echo 🚀 Pushing to GitHub...
:: Detect current branch
for /f "tokens=*" %%i in ('git rev-parse --abbrev-ref HEAD') do set branch=%%i

git push -u origin %branch% --force

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Push failed. 
    echo Possible causes:
    echo 1. No internet connection.
    echo 2. You need to login (run 'git login' or check credential manager).
    echo 3. The repository does not exist or you don't have access.
) else (
    echo.
    echo ✅ SUCCESS: All code has been sent to GitHub!
    echo 🌍 URL: https://github.com/kavyasriakkathi/TriGuard-AI
)

echo.
pause

