# NetworkTraffic Django 后端

## 项目结构
```
backend/
├── manage.py                 # Django管理脚本
├── requirements.txt          # Python依赖
├── .env                      # 环境变量配置
├── network_traffic/          # Django项目配置
│   ├── __init__.py
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 主URL配置
│   ├── wsgi.py              # WSGI配置
│   └── asgi.py              # ASGI配置
├── apps/                    # 应用模块
│   ├── authentication/      # 用户认证
│   ├── traffic/            # 流量管理
│   ├── model_analysis/     # 模型分析
│   └── dashboard/          # 数据统计
├── media/                   # 上传文件存储
├── static/                  # 静态文件
└── templates/               # 模板文件
```

## 安装和运行

### 1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 环境配置
复制 `.env.example` 到 `.env` 并配置：
```bash
cp .env.example .env
```

### 4. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户
```bash
python manage.py createsuperuser
```

### 6. 运行开发服务器
```bash
python manage.py runserver
```

## API 接口

### 认证接口
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户登出
- `POST /api/auth/refresh/` - 刷新Token

### 流量管理
- `GET /api/traffic/list/` - 获取流量列表
- `POST /api/traffic/upload/` - 上传流量文件
- `GET /api/traffic/statistics/` - 获取流量统计

### 模型分析
- `GET /api/model/analysis/` - 获取模型分析结果
- `POST /api/model/train/` - 训练模型
- `GET /api/model/status/` - 获取模型状态

### 数据统计
- `GET /api/dashboard/overview/` - 获取总览数据
- `GET /api/dashboard/trends/` - 获取趋势数据
- `GET /api/dashboard/alerts/` - 获取告警数据 