@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo Complete Deployment Control Script
echo ========================================
echo.
echo This script will:
echo 1. Build the backend (Django + API)
echo 2. Build the frontend (Vue.js)
echo 3. Start all services (MySQL, Backend, Frontend)
echo.
echo IMPORTANT NOTES:
echo - This process may take 10-20 minutes total
echo - Do not close any windows during the build process
echo - Each step will pause for confirmation before proceeding
echo.
echo Access URLs after deployment:
echo - Frontend: http://localhost:23456
echo - Backend: http://localhost:8000
echo - Database: localhost:3307
echo.
echo Test accounts:
echo - Admin: admin/123456
echo - Test User: yang/123456
echo.
pause

echo.
echo ========================================
echo Step 0: Setting up Conda Environment
echo ========================================
echo.
echo Preparing Conda environment...
call build-conda.bat
if %errorlevel% neq 0 (
    echo ERROR: Conda environment setup failed!
echo Please check the error messages above.
    pause
    exit /b 1
)
echo Conda environment ready ✓
echo.

echo ========================================
echo Step 1: Building Backend
echo ========================================
echo.
echo Starting backend build...
call build-backend.bat
if %errorlevel% neq 0 (
    echo ERROR: Backend build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo Backend build completed successfully ✓
echo.

echo ========================================
echo Step 2: Building Frontend
echo ========================================
echo.
echo Starting frontend build...
call build-frontend.bat
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo Frontend build completed successfully ✓
echo.

echo ========================================
echo Step 3: Starting Services
echo ========================================
echo.
echo Starting all services...
call start-services.bat
if %errorlevel% neq 0 (
    echo ERROR: Service startup failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo Service startup completed successfully ✓
echo.

echo ========================================
echo Deployment Completed Successfully!
echo ========================================
echo.
echo All components have been built and started:
echo ✓ Backend (Django API)
echo ✓ Frontend (Vue.js)
echo ✓ Database (MySQL)
echo.
echo Your application is now ready!
echo.
echo Access URLs:
echo - Frontend Application: http://localhost:23456
echo - Backend API: http://localhost:8000
echo - Admin Interface: http://localhost:8000/admin/
echo.
echo Test the application:
echo 1. Open http://localhost:23456 in your browser
echo 2. Login with admin/123456 or yang/123456
echo 3. Try creating a new chat session
echo 4. Test file upload and message sending
echo.
echo Management commands:
echo - Stop all services: docker-compose -f docker-compose.production.yml down
echo - View logs: docker-compose -f docker-compose.production.yml logs -f
echo - Restart services: docker-compose -f docker-compose.production.yml restart
echo.
echo ========================================
pause 