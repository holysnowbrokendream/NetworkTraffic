@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo Images Environment Configuration
echo ========================================
echo.

REM 获取本机IP地址
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /C:"IPv4"') do (
    set "HOST_IP=%%i"
    set "HOST_IP=!HOST_IP: =!"
    goto :found_ip
)

:found_ip
echo Detected host IP: !HOST_IP!
echo.

REM 创建环境变量文件
echo Creating .env file for images deployment...
(
echo # Images Environment Configuration
echo HOST_IP=!HOST_IP!
echo ALLOWED_HOSTS=localhost,127.0.0.1,!HOST_IP!,0.0.0.0,*
echo CSRF_TRUSTED_ORIGINS=http://localhost:23456,http://!HOST_IP!:23456,http://127.0.0.1:23456,http://0.0.0.0:23456
echo.
echo # Database Configuration
echo DB_NAME=network_traffic
echo DB_USER=nwt_user
echo DB_PASSWORD=123456
echo DB_HOST=mysql
echo DB_PORT=3306
) > ..\.env

echo Environment configuration created ✓
echo.
echo Next steps:
echo 1. Run start-services-images.bat to start services
echo 2. Access application at: http://!HOST_IP!:23456
echo.

pause
