# Backend后端
采用Django框架，与前端VUE进行分离

# 项目结构详解

## 整体结构
Backend/
├── NTBack/                          # Django项目根目录
│   ├── manage.py                    # Django管理脚本
│   ├── requirements.txt             # Python依赖包列表
│   ├── NTBack/                      # Django项目配置目录
│   │   ├── __init__.py             # Python包初始化文件
│   │   ├── settings.py             # Django项目设置文件
│   │   ├── urls.py                 # 主URL路由配置
│   │   ├── wsgi.py                 # WSGI应用配置
│   │   └── asgi.py                 # ASGI应用配置
│   ├── apps/                       # Django应用模块目录
│   ├── templates/                  # HTML模板目录
│   ├── static/                     # 静态文件目录
│   ├── media/                      # 媒体文件目录
│   └── logs/                       # 日志文件目录
└── README.md                       # 项目说明文档

## 核心配置文件

### manage.py
Django项目的管理脚本
用于运行各种Django命令（如启动服务器、数据库迁移等）
设置Django设置模块为NTBack.settings

### NTBack/settings.py
项目配置中心，包含所有Django设置
数据库配置: 使用MySQL数据库
安全设置: SECRET_KEY、DEBUG模式、ALLOWED_HOSTS
国际化: 支持多语言，默认英文
静态文件: CSS、JS、图片等静态资源
媒体文件: 用户上传的文件存储

### NTBack/urls.py
主URL路由配置
目前只配置了Django管理后台路由
需要添加各个应用的URL配置

### NTBack/wsgi.py & asgi.py
WSGI配置: 用于生产环境部署
ASGI配置: 支持异步Web应用
