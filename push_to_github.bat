@echo off
setlocal
title TriGuard AI - GitHub Uploader

echo ===================================================
echo 🛡️  TriGuard AI - GitHub Uploader
echo ===================================================
echo.

:: Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Git is not installed or not in your PATH.
    pause
    exit /b 1
)

echo [1/3] Staging changes...
git add .

echo [2/3] Committing changes...
set /p commit_msg="Enter commit message (or press Enter for 'Update TriGuard AI'): "
if "%commit_msg%"=="" set commit_msg=Update TriGuard AI
git commit -m "%commit_msg%"

echo [3/3] Pushing to GitHub...
:: Try to detect current branch
for /f "tokens=*" %%i in ('git rev-parse --abbrev-ref HEAD') do set branch=%%i
echo 🚀 Pushing to branch: %branch%

git push origin %branch%
if %errorlevel% neq 0 (
    echo ❌ ERROR: Push failed. Check your internet connection or GitHub permissions.
) else (
    echo ✅ Successfully sent to GitHub!
)

echo.
pause

