@echo off
chcp 65001 >nul
echo 🚀 设置开发环境变量...

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 运行Python脚本设置环境变量
python setup_dev_env.py

REM 检查是否成功创建.env文件
if exist .env (
    echo.
    echo ✅ 环境变量设置完成！
    echo.
    echo 📋 当前配置:
    echo   数据库: localhost:3306
    echo   用户名: nwt_user
    echo   密码: 123456
    echo   数据库名: network_traffic
    echo.
    echo 📝 下一步操作:
    echo   1. 确保MySQL服务正在运行
    echo   2. 创建数据库: CREATE DATABASE network_traffic;
    echo   3. 运行迁移: python manage.py migrate
    echo   4. 启动服务器: python manage.py runserver
    echo.
) else (
    echo ❌ 环境变量设置失败
)

pause 