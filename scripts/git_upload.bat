@echo off
chcp 65001 >nul
echo ============================================================
echo Kunnix Git Upload Script
echo ============================================================
echo.

cd /d "%~dp0.."

echo [1/5] Initializing Git repository...
git init
if errorlevel 1 (
    echo [ERROR] Git init failed!
    pause
    exit /b 1
)
echo [OK] Git initialized
echo.

echo [2/5] Adding all files...
git add .
if errorlevel 1 (
    echo [ERROR] Git add failed!
    pause
    exit /b 1
)
echo [OK] Files added
echo.

echo [3/5] Committing changes...
git commit -m "Initial commit: Kunnix v1.0.0 - Memory ^& Task Scheduling System"
if errorlevel 1 (
    echo [ERROR] Git commit failed!
    pause
    exit /b 1
)
echo [OK] Changes committed
echo.

echo [4/5] Adding remote repository...
git remote add origin https://github.com/kunnix-ai/memory-task-system.git
if errorlevel 1 (
    echo [WARN] Remote may already exist, trying to update...
    git remote set-url origin https://github.com/kunnix-ai/memory-task-system.git
)
echo [OK] Remote added
echo.

echo [5/5] Pushing to GitHub...
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo [ERROR] Git push failed!
    echo Please check:
    echo   1. GitHub repository exists
    echo   2. You have write permission
    echo   3. Repository is empty
    pause
    exit /b 1
)
echo [OK] Pushed to GitHub
echo.

echo ============================================================
echo [SUCCESS] Kunnix v1.0.0 uploaded successfully!
echo ============================================================
echo.
echo Repository URL: https://github.com/kunnix-ai/memory-task-system
echo.
pause
