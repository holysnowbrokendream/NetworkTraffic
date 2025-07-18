"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# 设置Django项目的settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 获取ASGI应用对象，供ASGI服务器启动
application = get_asgi_application()
