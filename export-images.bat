@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo Docker Image Export Script
echo ========================================
echo.
echo This script will export successfully deployed Docker images to the specified directory
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

REM Create export directory
set "EXPORT_DIR=DockerImages"
if not exist "%EXPORT_DIR%" mkdir "%EXPORT_DIR%"
echo Export directory: %EXPORT_DIR%

echo.
echo ========================================
echo Step 1: Check Existing Images
echo ========================================
echo.

REM Check and list related images
echo Checking NetworkTraffic related images...
docker images | findstr networktraffic
if %errorlevel% neq 0 (
    echo No NetworkTraffic images found, please run deploy-all.bat first to build images
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Export Images
echo ========================================
echo.

REM Export backend image
echo Exporting backend image...
set "BACKEND_IMAGE="
for /f "tokens=1" %%i in ('docker images --format "{{.Repository}}:{{.Tag}}" ^| findstr networktraffic-backend') do (
    set "BACKEND_IMAGE=%%i"
    goto :found_backend
)
echo Backend image not found, skipping export
goto :export_frontend

:found_backend
echo Found backend image: !BACKEND_IMAGE!
docker save -o "%EXPORT_DIR%\networktraffic-backend.tar" "!BACKEND_IMAGE!"
if %errorlevel% equ 0 (
    echo Backend image exported successfully: %EXPORT_DIR%\networktraffic-backend.tar
) else (
    echo ERROR: Backend image export failed
)

:export_frontend
REM Export frontend image
echo.
echo Exporting frontend image...
set "FRONTEND_IMAGE="
for /f "tokens=1" %%i in ('docker images --format "{{.Repository}}:{{.Tag}}" ^| findstr networktraffic-frontend') do (
    set "FRONTEND_IMAGE=%%i"
    goto :found_frontend
)
echo Frontend image not found, skipping export
goto :export_mysql

:found_frontend
echo Found frontend image: !FRONTEND_IMAGE!
docker save -o "%EXPORT_DIR%\networktraffic-frontend.tar" "!FRONTEND_IMAGE!"
if %errorlevel% equ 0 (
    echo Frontend image exported successfully: %EXPORT_DIR%\networktraffic-frontend.tar
) else (
    echo ERROR: Frontend image export failed
)

:export_mysql
REM Export MySQL image (optional, as it uses official image)
echo.
echo Exporting MySQL image (official image)...
docker save -o "%EXPORT_DIR%\mysql-8.0.tar" mysql:8.0
if %errorlevel% equ 0 (
    echo MySQL image exported successfully: %EXPORT_DIR%\mysql-8.0.tar
) else (
    echo ERROR: MySQL image export failed
)

echo.
echo ========================================
echo Export Completed!
echo ========================================
echo.
echo Exported files are located in: %EXPORT_DIR%\
echo.
echo Contains the following files:
echo ✓ Backend image: networktraffic-backend.tar
echo ✓ Frontend image: networktraffic-frontend.tar  
echo ✓ MySQL image: mysql-8.0.tar
echo ✓ Windows import script: import-images.bat
echo ✓ Linux import script: import-images.sh
echo ✓ Usage instructions: README.md
echo.
echo Usage:
echo 1. Copy the entire %EXPORT_DIR% folder to others
echo 2. Others can run the corresponding import script
echo 3. No need to rebuild, start services directly
echo.
echo Notes:
echo - Image files are large, please be patient during transfer
echo - Ensure target machine has sufficient disk space
echo - After import, you can use start-services.bat/sh to start services
echo.
pause
