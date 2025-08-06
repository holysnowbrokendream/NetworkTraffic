@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo Windows防火墙配置脚本
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 需要管理员权限运行此脚本
    echo 请右键点击此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo ✅ 管理员权限检查通过

REM 配置8000端口防火墙规则
echo 🔧 配置8000端口防火墙规则...
netsh advfirewall firewall add rule name="NetworkTraffic Backend" dir=in action=allow protocol=TCP localport=8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 8000端口防火墙规则配置成功
) else (
    echo ⚠️  8000端口防火墙规则可能已存在
)

REM 配置23456端口防火墙规则
echo 🔧 配置23456端口防火墙规则...
netsh advfirewall firewall add rule name="NetworkTraffic Frontend" dir=in action=allow protocol=TCP localport=23456 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 23456端口防火墙规则配置成功
) else (
    echo ⚠️  23456端口防火墙规则可能已存在
)

REM 配置3307端口防火墙规则（数据库，可选）
echo 🔧 配置3307端口防火墙规则（数据库）...
netsh advfirewall firewall add rule name="NetworkTraffic Database" dir=in action=allow protocol=TCP localport=3307 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 3307端口防火墙规则配置成功
) else (
    echo ⚠️  3307端口防火墙规则可能已存在
)

echo.
echo ========================================
echo 防火墙配置完成!
echo ========================================
echo.
echo ✅ 已配置以下端口:
echo - 8000: 后端API服务
echo - 23456: 前端Web服务
echo - 3307: 数据库服务（可选）
echo.
echo 💡 现在同一内网下的设备可以访问您的服务了
echo.
pause 