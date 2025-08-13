@echo off
chcp 65001 >nul
echo 🚀 完整开发环境设置...

REM 激活虚拟环境
call .venv\Scripts\activate.bat

echo.
echo 📝 步骤1: 设置环境变量...
python setup_dev_env.py

echo.
echo 📝 步骤2: 初始化数据库...
python init_database.py

echo.
echo 📝 步骤3: 运行数据库迁移...
python manage.py migrate

echo.
echo 📝 步骤4: 收集静态文件...
python manage.py collectstatic --noinput

echo.
echo ✅ 开发环境设置完成！
echo.
echo 📋 当前配置:
echo   数据库: localhost:3307/network_traffic
echo   用户名: nwt_user
echo   密码: 123456
echo   Django: DEBUG=True
echo.
echo 🚀 启动开发服务器:
echo   python manage.py runserver
echo.
echo 💡 其他常用命令:
echo   - 创建超级用户: python manage.py createsuperuser
echo   - 进入Django shell: python manage.py shell
echo   - 查看帮助: python manage.py help
echo.

pause 