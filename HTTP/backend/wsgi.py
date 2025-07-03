"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置Django项目的settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 获取WSGI应用对象，供服务器启动
application = get_wsgi_application()
