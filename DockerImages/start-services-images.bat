@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo Images Services Startup Script
echo ========================================
echo.

REM 检查.env文件是否存在
if not exist "..\.env" (
    echo ❌ .env file not found!
    echo Please run images-setup.bat first to configure the environment.
    pause
    exit /b 1
)

REM 检查Docker是否运行
echo Checking Docker status...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running or not installed!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo Docker is running ✓

REM 检查Docker镜像是否存在
echo Checking Docker images...
docker images | findstr networktraffic >nul
if %errorlevel% neq 0 (
    echo ❌ NetworkTraffic Docker images not found!
    echo Please import Docker images first using import-images.bat
    pause
    exit /b 1
)
echo Docker images found ✓

REM 创建必要的目录
echo Creating necessary directories...
if not exist "..\config" mkdir ..\config
if not exist "..\logs" mkdir ..\logs
if not exist "..\HTTP\media" mkdir ..\HTTP\media
if not exist "..\HTTP\staticfiles" mkdir ..\HTTP\staticfiles
if not exist "..\mysql\init" mkdir ..\mysql\init
if not exist "..\nginx\ssl" mkdir ..\nginx\ssl
echo Directories created ✓

REM 启动服务
echo.
echo 🚀 Starting NetworkTraffic services...
docker-compose -f ..\docker-compose.client.yml up -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ Services started successfully!
    echo.
    echo 📋 Service Status:
    echo   MySQL: localhost:3306
    echo   Backend: localhost:8000
    echo   Frontend: localhost:23456
    echo   Nginx: localhost:80
    echo.
    echo 🌐 Access URLs:
    echo   Frontend: http://localhost:23456
    echo   Backend API: http://localhost:8000
    echo   Admin: http://localhost:8000/admin/
    echo.
    echo 💡 To view logs: docker-compose -f ..\docker-compose.client.yml logs -f
    echo 💡 To stop services: docker-compose -f ..\docker-compose.client.yml down
    echo.
) else (
    echo ❌ Failed to start services!
    echo Please check the error messages above.
)

pause
