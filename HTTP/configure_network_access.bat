@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo 网络访问配置脚本
echo ========================================
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python并确保在PATH中
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

REM 运行网络配置脚本
echo.
echo 🚀 开始配置网络访问...
python network_access_config.py

if %errorlevel% neq 0 (
    echo ❌ 网络配置脚本执行失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 网络访问配置完成!
echo ========================================
echo.
echo 💡 下一步操作:
echo 1. 重新构建后端: build-backend.bat
echo 2. 重新启动服务: start-services.bat
echo 3. 测试网络访问
echo.
echo ⚠️  注意事项:
echo - 确保防火墙允许8000和23456端口
echo - 同一内网设备可以通过本机IP访问
echo - 如果无法访问，请检查防火墙设置
echo.
pause 