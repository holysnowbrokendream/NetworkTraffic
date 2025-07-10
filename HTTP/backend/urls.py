"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userauth import views as userauth_views

# 项目主路由配置
urlpatterns = [
    path('admin/', admin.site.urls),  # Django后台管理
    path('api/llm/chat/', userauth_views.llm_chat),
    path('api/llm/upload/', userauth_views.llm_upload),
    path('', include('userauth.urls')),  # 用户认证相关接口
    path('api/modeltask/', include('modeltask.urls')),  # 模型任务相关接口
]
