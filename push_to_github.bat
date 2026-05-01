@echo off
echo ===================================================
echo 🚀 TriGuard AI - GitHub Auto-Push Script
echo ===================================================
echo.

echo [1/3] Adding all files to staging...
git add .
if %errorlevel% neq 0 (
    echo ❌ Failed to add files. Make sure git is installed.
    pause
    exit /b %errorlevel%
)
echo ✅ Files added successfully.
echo.

echo [2/3] Committing the final hackathon version...
git commit -m "feat: complete TriGuard AI with verification scripts and final UI"
if %errorlevel% neq 0 (
    echo ⚠️ Nothing to commit or commit failed.
) else (
    echo ✅ Commit successful.
)
echo.

echo [3/3] Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ⚠️ Push to main failed. Trying to push to master instead...
    git push origin master
    if %errorlevel% neq 0 (
        echo ❌ Push to master also failed. Please check your GitHub permissions or branch name.
        pause
        exit /b %errorlevel%
    )
)

echo.
echo ===================================================
echo 🏆 SUCCESS: Your code has been sent to GitHub!
echo ===================================================
pause
