@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo Services Startup Script
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

REM Check if required images exist
echo Checking required Docker images...
docker images | findstr networktraffic-backend >nul
if %errorlevel% neq 0 (
    echo ERROR: Backend image not found!
    echo Please run build-backend.bat first.
    pause
    exit /b 1
)

docker images | findstr networktraffic-frontend >nul
if %errorlevel% neq 0 (
    echo ERROR: Frontend image not found!
    echo Please run build-frontend.bat first.
    pause
    exit /b 1
)
echo All required images found ✓

REM Stop all existing services
echo Stopping all existing services...
docker-compose -f docker-compose.production.yml down
echo All services stopped ✓

REM Start services step by step
echo Starting MySQL database...
docker-compose -f docker-compose.production.yml up -d mysql
if %errorlevel% neq 0 (
    echo ERROR: Failed to start MySQL!
    pause
    exit /b 1
)

echo Waiting for MySQL to be ready...
echo Checking MySQL status...
for /l %%i in (1,1,20) do (
    timeout /t 1 /nobreak >nul
    docker-compose -f docker-compose.production.yml ps mysql | findstr "healthy" >nul
    if !errorlevel! equ 0 (
        echo MySQL is ready ✓
        goto mysql_ready
    )
    echo Waiting for MySQL... %%i/20
)
echo WARNING: MySQL may not be fully ready
:mysql_ready

echo Starting backend service...
docker-compose -f docker-compose.production.yml up -d backend
if %errorlevel% neq 0 (
    echo ERROR: Failed to start backend!
    pause
    exit /b 1
)

echo Waiting for backend to be ready...
echo Checking backend status...
for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    curl -s http://localhost:8000/login/ >nul 2>&1
    if !errorlevel! equ 0 (
        echo Backend is ready ✓
        goto backend_ready
    )
    echo Waiting for backend... %%i/30
)
echo WARNING: Backend may not be fully ready
:backend_ready

echo Starting frontend service...
docker-compose -f docker-compose.production.yml up -d frontend
if %errorlevel% neq 0 (
    echo ERROR: Failed to start frontend!
    pause
    exit /b 1
)

echo Waiting for frontend to be ready...
echo Checking frontend status...
for /l %%i in (1,1,20) do (
    timeout /t 1 /nobreak >nul
    curl -s http://localhost:23456 >nul 2>&1
    if !errorlevel! equ 0 (
        echo Frontend is ready ✓
        goto frontend_ready
    )
    echo Waiting for frontend... %%i/20
)
echo WARNING: Frontend may not be fully ready
:frontend_ready

REM Note: Nginx is commented out in docker-compose.yml as frontend container includes nginx
echo Note: Frontend container includes nginx, no separate nginx container needed

echo.
echo Checking final service status...
docker-compose -f docker-compose.production.yml ps

REM Test backend API functionality
echo.
echo Testing backend API...
timeout /t 3 /nobreak >nul
curl -s http://localhost:8000/login/ >nul 2>&1
if %errorlevel% equ 0 (
    echo Backend API is responding ✓
) else (
    echo WARNING: Backend API may not be ready yet
)

REM Create default admin user if not exists
echo.
echo Creating default admin user...
docker exec network_traffic_backend_prod python manage.py shell -c "from django.contrib.auth.models import User; User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})" 2>nul
if %errorlevel% equ 0 (
    echo Default admin user created/verified ✓
    echo Username: admin
    echo Password: 123456
) else (
    echo WARNING: Could not create default admin user
)

REM Create test user if not exists
echo Creating test user...
docker exec network_traffic_backend_prod python manage.py shell -c "from django.contrib.auth.models import User; User.objects.get_or_create(username='yang', defaults={'is_staff': False, 'is_superuser': False})" 2>nul
if %errorlevel% equ 0 (
    echo Test user created/verified ✓
    echo Username: yang
    echo Password: 123456
) else (
    echo WARNING: Could not create test user
)

echo.
echo ========================================
echo Services Started Successfully!
echo ========================================
echo.
echo Access URLs:
echo   - Frontend Application: http://localhost:23456
echo   - Backend API: http://localhost:8000/api/
echo   - Admin Interface: http://localhost:8000/admin/
echo   - Backend Direct: http://localhost:8000
echo   - Database: localhost:3307
echo.
echo Test Accounts:
echo   - Admin: admin/123456
echo   - Test User: yang/123456
echo.
echo Management Commands:
echo   - Stop services: docker-compose -f docker-compose.production.yml down
echo   - View logs: docker-compose -f docker-compose.production.yml logs -f
echo   - Restart: docker-compose -f docker-compose.production.yml restart
echo.
echo Troubleshooting:
echo   - If frontend can't connect to backend, check axios baseURL in main.js
echo   - If ports are busy, check: netstat -ano ^| findstr :23456
echo   - If backend fails, check: docker logs network_traffic_backend_prod
echo   - If database fails, check: docker logs network_traffic_mysql_prod
echo.
echo Test the application:
echo   1. Open http://localhost:23456 in your browser
echo   2. Login with admin/123456 or yang/123456
echo   3. Try creating a new chat session
echo   4. Test file upload and message sending
echo ========================================
echo.
pause 