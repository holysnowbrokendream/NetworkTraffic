@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo Backend Build Script
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

REM Create production environment file if not exists
if not exist ".env" (
    echo Creating production environment configuration...
    (
    echo # ========================================
    echo # Production Environment Configuration
    echo # ========================================
    echo.
    echo # Database Configuration
    echo DB_NAME=NetworkTraffic
    echo DB_USER=nwt_user
    echo DB_PASSWORD=123456
    echo DB_HOST=mysql
    echo DB_PORT=3306
    echo MYSQL_ROOT_PASSWORD=123456
    echo.
    echo # Django Configuration
    echo SECRET_KEY=network-traffic-production-secret-key-2024-change-this-in-production
    echo DEBUG=False
    echo ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com,www.your-domain.com
    echo CSRF_TRUSTED_ORIGINS=http://localhost:3001,https://your-domain.com,https://www.your-domain.com
    echo.
    echo # Frontend Configuration
    echo VITE_API_BASE_URL=http://localhost:8000
    echo.
    echo # Deployment Configuration
    echo ENVIRONMENT=production
    echo.
    echo # Nginx Configuration
    echo NGINX_SERVER_NAME=localhost
    echo NGINX_SSL_CERT=/etc/nginx/ssl/cert.pem
    echo NGINX_SSL_KEY=/etc/nginx/ssl/key.pem
    ) > .env
    echo Production .env file created ✓
)

REM Create necessary directories
echo Creating production directories...
if not exist "HTTP\media" mkdir HTTP\media
if not exist "HTTP\temp" mkdir HTTP\temp
if not exist "HTTP\staticfiles" mkdir HTTP\staticfiles
if not exist "mysql\init" mkdir mysql\init
if not exist "nginx\ssl" mkdir nginx\ssl
if not exist "logs" mkdir logs
echo Directories created ✓

REM Stop existing backend service
echo Stopping existing backend service...
REM Check if backend container exists before trying to stop it
docker-compose -f docker-compose.production.yml ps backend 2>nul | findstr "Up\|Exit" >nul
if %errorlevel% equ 0 (
    echo Backend container found, stopping it...
    docker-compose -f docker-compose.production.yml stop backend 2>nul
    docker-compose -f docker-compose.production.yml rm -f backend 2>nul
    echo Backend service stopped ✓
) else (
    echo No existing backend container found, skipping stop operation ✓
)

REM Build backend image
echo Building backend Docker image...
echo This may take 5-10 minutes for the first build...
echo IMPORTANT: Do not close this window during the build process!
echo.

docker-compose -f docker-compose.production.yml build backend
if %errorlevel% neq 0 (
    echo ERROR: Backend Docker build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo Backend image built successfully ✓

REM Verify backend image was built
echo Verifying backend image...
docker images | findstr networktraffic-backend >nul
if %errorlevel% neq 0 (
    echo ERROR: Backend Docker image not found after build!
    pause
    exit /b 1
)
echo Backend image verified ✓

echo.
echo ========================================
echo Backend Build Completed Successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Run build-frontend.bat to build the frontend
echo 2. Run start-services.bat to start all services
echo.
pause 