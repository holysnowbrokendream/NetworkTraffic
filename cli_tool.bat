@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 网络流量分析项目CLI工具启动脚本
echo 🔧 网络流量分析项目CLI工具启动脚本
echo.

REM 检查Python环境
set PYTHON_CMD=python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

REM 检查requests库
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装requests库...
    python -m pip install requests
    if errorlevel 1 (
        echo ❌ 安装requests库失败
        pause
        exit /b 1
    )
)

REM 检查参数
if "%1"=="" (
    REM 无参数，启动交互模式
    echo 🚀 启动交互模式...
    python cli_tool.py
    goto :end
)

if "%1"=="interactive" (
    REM 交互模式
    echo 🚀 启动交互模式...
    python cli_tool.py
    goto :end
)

if "%1"=="quick" (
    REM 快速模式
    echo 🚀 启动快速模式...
    python quick_cli.py %2 %3 %4 %5 %6 %7 %8 %9
    goto :end
)

if "%1"=="help" (
    REM 显示帮助
    echo 📖 CLI工具帮助信息:
    echo.
    echo 用法:
    echo   cli_tool.bat                    - 启动交互模式
    echo   cli_tool.bat interactive        - 启动交互模式
    echo   cli_tool.bat quick analyze <文件路径>  - 快速分析PCAP文件
    echo   cli_tool.bat quick generate <提示词>   - 快速生成PCAP文件
    echo   cli_tool.bat help               - 显示此帮助信息
    echo.
    echo 📁 文件路径支持:
    echo   - 绝对路径: C:/path/to/file.pcap
    echo   - 相对路径: ./file.pcap
    echo   - 通配符: *.pcap (将使用第一个匹配的文件)
    echo.
    echo 💡 提示: 在Windows系统中，建议使用正斜杠(/)而不是反斜杠(\\)来避免路径问题
    goto :end
)

REM 其他参数，传递给Python脚本
echo 🚀 执行命令: %*
python cli_tool.py %*

:end
echo.
echo 👋 CLI工具执行完成
pause 