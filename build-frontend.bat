@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo Frontend Build Script
echo ========================================

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

REM Check if Node.js is available
echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js and try again.
    pause
    exit /b 1
)
echo Node.js is available ✓

REM Check if npm is available
echo Checking npm...
call npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm is not installed or not in PATH!
    echo Please install npm and try again.
    pause
    exit /b 1
)
echo npm is available ✓

REM Stop existing frontend service
echo Stopping existing frontend service...
REM Check if frontend container exists before trying to stop it
docker-compose -f docker-compose.production.yml ps frontend 2>nul | findstr "Up\|Exit" >nul
if %errorlevel% equ 0 (
    echo Frontend container found, stopping it...
    docker-compose -f docker-compose.production.yml stop frontend 2>nul
    docker-compose -f docker-compose.production.yml rm -f frontend 2>nul
    echo Frontend service stopped ✓
) else (
    echo No existing frontend container found, skipping stop operation ✓
)

REM Build frontend application
echo Building frontend application...
cd UI
if exist "dist" rmdir /s /q "dist"
echo Installing npm dependencies...
echo This may take several minutes...
timeout /t 2 >nul
call npm install --no-audit --no-fund
if %errorlevel% neq 0 (
    echo ERROR: npm install failed!
    echo Trying alternative approach...
    call npm cache clean --force 2>nul
    call npm install --no-audit --no-fund
    if %errorlevel% neq 0 (
        echo ERROR: npm install still failed after cache clean!
        cd ..
        pause
        exit /b 1
    )
)
echo npm dependencies installed ✓

echo Building frontend with Vite...
echo This may take 1-3 minutes...
timeout /t 2 >nul
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed!
    cd ..
    pause
    exit /b 1
)
cd ..
echo Frontend built successfully ✓

REM Build frontend Docker image
echo Building frontend Docker image...
echo This may take 2-5 minutes for the first build...
echo IMPORTANT: Do not close this window during the build process!
echo.

docker-compose -f docker-compose.production.yml build frontend
if %errorlevel% neq 0 (
    echo ERROR: Frontend Docker build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo Frontend image built successfully ✓

REM Verify frontend image was built
echo Verifying frontend image...
docker images | findstr networktraffic-frontend >nul
if %errorlevel% neq 0 (
    echo ERROR: Frontend Docker image not found after build!
    pause
    exit /b 1
)
echo Frontend image verified ✓

echo.
echo ========================================
echo Frontend Build Completed Successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Run build-backend.bat to build the backend (if not done)
echo 2. Run start-services.bat to start all services
echo.
pause 