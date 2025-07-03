# Backend后端
采用Django框架，与前端VUE进行分离（还没有实现）

---

## 项目结构详解

### 整体结构
Backend/ 
├── NTBack/                          # Django项目根目录 
│   ├── manage.py                    # Django管理脚本，项目入口
│   ├── requirements.txt             # Python依赖包列表
│   ├── NTBack/                      # Django项目配置目录 
│   │   ├── __init__.py              # Python包初始化文件
│   │   ├── settings.py              # Django项目设置文件，包含数据库、静态文件等配置
│   │   ├── urls.py                  # 主URL路由配置，分发到各个app
│   │   ├── wsgi.py                  # WSGI应用配置，生产环境部署用
│   │   └── asgi.py                  # ASGI应用配置，支持异步服务
│   ├── apps/                        # Django应用模块目录
│   │   ├── Sampleapp/               # 示例应用
│   │   │   ├── __init__.py          # 应用包初始化
│   │   │   ├── admin.py             # 后台管理注册
│   │   │   ├── apps.py              # 应用配置
│   │   │   ├── migrations/          # 数据库迁移文件目录
│   │   │   │   └── __init__.py      # 迁移包初始化
│   │   │   ├── models.py            # 数据模型定义（如Sample、UserAccount等）
│   │   │   ├── tests.py             # 单元测试
│   │   │   ├── urls.py              # 应用内URL路由
│   │   │   └── views.py             # 视图函数（如首页、注册、登录、个人主页等）
│   ├── templates/                   # HTML模板目录
│   │   ├── Home.html                # 首页模板，系统介绍、注册/登录入口
│   │   ├── Signup.html              # 注册页面模板
│   │   ├── Login.html               # 登录页面模板
│   │   ├── Dashboard.html           # 个人主页模板，展示和修改用户信息
│   │   ├── App.html                 # 预留页面
│   │   ├── Traffic.html             # 预留页面
│   │   ├── Settings.html            # 预留页面
│   │   ├── Model.html               # 预留页面
│   │   └── Sample.html              # 预留页面
│   ├── static/                      # 静态文件目录（CSS、JS、图片等）
│   ├── media/                       # 媒体文件目录（用户上传文件）
│   └── logs/                        # 日志文件目录
└── README.md                        # 项目说明文档

---

## 核心配置文件

### manage.py
- Django项目的管理脚本
- 用于运行各种Django命令（如启动服务器、数据库迁移等）
- 设置Django设置模块为NTBack.settings

### NTBack/settings.py
- 项目配置中心，包含所有Django设置
- 数据库配置: 使用MySQL数据库（可切换为SQLite测试）
- 安全设置: SECRET_KEY、DEBUG模式、ALLOWED_HOSTS
- 国际化: 支持多语言，默认英文
- 静态文件: CSS、JS、图片等静态资源
- 媒体文件: 用户上传的文件存储

**注意：数据库需要额外进行配置，请将 NTBack/settings.py 中的 DATABASES 更改为本地配置，并在配置完成后运行，以更新自动化数据库迁移并执行
```bash
python manage.py makemigrations
python manage.py migrate
```

### NTBack/urls.py
- 主URL路由配置
- 已配置Django管理后台路由和各个应用的URL

### NTBack/wsgi.py & asgi.py
- WSGI配置: 用于生产环境部署
- ASGI配置: 支持异步Web应用

## 应用文件

### apps/Sampleapp/models
- 定义了Sample、UserAccount等数据模型
- UserAccount支持用户名、邮箱、手机号唯一性校验，支持用户类型、注册时间、更新时间等字段

### apps/Sampleapp/views
- 包含首页、注册、登录、登出、个人主页（Dashboard）等视图
- 支持表单验证、信息修改、会话管理等功能

### apps/Sampleapp/urls
- 配置了home、signup、login、logout、dashboard等路由

### apps/Sampleapp/apps
- 应用配置文件

### apps/Sampleapp/migrations
- 数据库迁移文件目录

## 模板/网页文件（测试用，与VUE对接时更改）

### templates/Home.html
- 首页，展示系统介绍、注册和登录入口

### templates/Signup.html
- 用户注册页面，支持表单验证和错误提示

### templates/Login.html
- 用户登录页面，支持多种登录方式（用户名、手机号、邮箱）

### tempaltes/Dashboard.html
- 个人主页，展示用户信息，支持信息修改和退出登录
