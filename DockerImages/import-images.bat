@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo Docker Image Import Script (Windows)
echo ========================================
echo.
echo This script will import pre-built Docker images
echo.

REM Check if Docker is running
echo Checking Docker status...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running or not installed!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo Docker is running ✓

REM Import images
echo Starting image import...
echo.

if exist "networktraffic-backend.tar" (
    echo Importing backend image...
    docker load -i "networktraffic-backend.tar"
    if %errorlevel% equ 0 (
        echo Backend image imported successfully ✓
    ) else (
        echo ERROR: Backend image import failed
    )
)

if exist "networktraffic-frontend.tar" (
    echo Importing frontend image...
    docker load -i "networktraffic-frontend.tar"
    if %errorlevel% equ 0 (
        echo Frontend image imported successfully ✓
    ) else (
        echo ERROR: Frontend image import failed
    )
)

if exist "mysql-8.0.tar" (
    echo Importing MySQL image...
    docker load -i "mysql-8.0.tar"
    if %errorlevel% equ 0 (
        echo MySQL image imported successfully ✓
    ) else (
        echo ERROR: MySQL image import failed
    )
)

echo.
echo ========================================
echo Step 2: Create Required Directories
echo ========================================
echo.

echo Creating necessary directories for the application...
cd ..

REM Create necessary directories
if not exist "HTTP\media" mkdir HTTP\media
if not exist "HTTP\temp" mkdir HTTP\temp
if not exist "HTTP\staticfiles" mkdir HTTP\staticfiles
if not exist "mysql\init" mkdir mysql\init
if not exist "nginx\ssl" mkdir nginx\ssl
if not exist "logs" mkdir logs
echo Directories created ✓

echo.
echo ========================================
echo Image Import Completed!
echo ========================================
echo.
echo Next steps:
echo 1. Ensure .env configuration file exists
echo 2. Run start-services.bat to start services
echo.
pause
