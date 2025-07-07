from django.urls import path
from . import views

urlpatterns = [
    # API端点
    path('api/home/', views.home_api, name='home_api'),
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/user/', views.user_info_api, name='user_info_api'),
    path('api/user/update/', views.update_user_api, name='update_user_api'),
    
    # CSRF令牌端点（用于前端获取CSRF令牌）
    path('api/csrf/', views.get_csrf_token, name='csrf_token'),
]


