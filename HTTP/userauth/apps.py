from django.apps import AppConfig

# userauth应用的配置类
class UserauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # 主键类型
    name = 'userauth'  # 应用名称
