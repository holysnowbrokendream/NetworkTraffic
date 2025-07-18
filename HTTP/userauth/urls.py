from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# 用户认证相关接口路由配置
urlpatterns = [
    path('login/', views.login, name='login'),  # 用户登录接口
    path('register/', views.register, name='register'),  # 用户注册接口
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT获取token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT刷新token
] 