# 🌐 NetworkTraffic 网络流量分析系统

---

## 📋 目录

1. [项目概述](#项目概述)
2. [系统要求](#系统要求)
3. [环境准备](#环境准备)
4. [快速部署](#快速部署)
5. [脚本使用指南](#脚本使用指南)
6. [服务管理](#服务管理)
7. [故障排除](#故障排除)
8. [配置说明](#配置说明)

---

## 🎯 项目概述

NetworkTraffic 是一个基于 Django + Vue.js 的网络流量分析系统，采用 Docker 容器化部署。

### 项目结构概览

| 目录       | 说明 |
|------------|------|
| `Model/`   | 大模型微调相关代码 |
| `UI/`      | 前端页面（Vue 项目） |
| `HTTP/`    | 后端服务代码（Django / Python） |

### 技术栈

- **前端**: Vue.js + Vite
- **后端**: Python + Django + DRF
- **数据库**: MySQL 8.0
- **部署**: Docker + Docker Compose
- **模型**: Python, Transformers, HuggingFace, PyTorch

---

## 🖥️ 系统要求

### 最低配置
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **内存**: 8GB RAM
- **存储**: 20GB 可用空间
- **网络**: 稳定的互联网连接

### 必需软件
- **Docker Desktop**: 版本 20.10+ 
- **Node.js**: 版本 18.0+ (用于前端构建)

### 可选软件
- **Git**: 版本 2.30+ (用于代码管理，如果从仓库下载代码则需要)

---

## 🔧 环境准备

### 1. 安装 Docker Desktop

**Windows 用户:**
1. 访问 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. 下载并安装 Docker Desktop
3. 启动 Docker Desktop
4. 确保 Docker 服务正在运行

**验证安装:**
```bash
docker --version
docker-compose --version
```

### 2. 安装 Node.js

**Windows 用户:**
1. 访问 [Node.js 官网](https://nodejs.org/)
2. 下载 LTS 版本 (推荐 18.x 或更高)
3. 安装 Node.js (包含 npm)

**验证安装:**
```bash
node --version
npm --version
```

### 3. 获取项目代码

**方案 A: 使用 Git (推荐)**
```bash
git clone <项目仓库地址>
cd NetworkTraffic
```

**方案 B: 直接下载**
1. 访问项目仓库页面
2. 点击 "Code" → "Download ZIP"
3. 解压到本地目录
4. 重命名为 `NetworkTraffic`

---

## 🚀 快速部署

### 🌐 内网部署

**如需将系统部署到内网环境，使同一局域网内的其他设备能够访问，请先查看详细的内网部署指南：**

📖 **[内网部署指南.md](内网部署指南.md)**

在网络与防火墙配置完成后，再运行后续部署脚本

### 一键部署 (推荐)

1. **运行一键部署脚本:**
   ```bash
   deploy-all.bat
   ```

2. **等待部署完成** (约 10-20 分钟)
   - 自动构建后端 (Django)
   - 自动构建前端 (Vue.js)
   - 自动启动所有服务

3. **访问应用:**
   - 前端应用: http://localhost:23456
   - 后端API: http://localhost:8000
   - 管理界面: http://localhost:8000/admin/

4. **测试账户:**
   - 管理员: `admin` / `123456`
   - 测试用户: `yang` / `123456`

---


## 🛠️ 脚本使用指南

### 可用的部署脚本

#### 1. 完整部署脚本
- **`deploy-all.bat`** - 一键完整部署脚本
  - 构建后端 (Django API)
  - 构建前端 (Vue.js)
  - 启动所有服务 (MySQL, Backend, Frontend)
  - 创建默认用户账户
  - 测试API功能

#### 2. 分步构建脚本
- **`build-backend.bat`** - 构建后端Docker镜像
- **`build-frontend.bat`** - 构建前端应用和Docker镜像

#### 3. 服务管理脚本
- **`start-services.bat`** - 启动所有服务
  - 按顺序启动 MySQL → Backend → Frontend
  - 包含健康检查和等待机制
  - 创建默认用户账户
  - 测试API功能

---

## 🛠️ 服务管理

### 查看服务状态

```bash
docker-compose -f docker-compose.production.yml ps
```

### 查看服务日志

```bash
# 查看所有服务日志
docker-compose -f docker-compose.production.yml logs -f

# 查看特定服务日志
docker-compose -f docker-compose.production.yml logs -f backend
docker-compose -f docker-compose.production.yml logs -f frontend
docker-compose -f docker-compose.production.yml logs -f mysql
```

### 重启服务

```bash
# 重启所有服务
docker-compose -f docker-compose.production.yml restart

# 重启特定服务
docker-compose -f docker-compose.production.yml restart backend
docker-compose -f docker-compose.production.yml restart frontend
```

### 停止服务

```bash
docker-compose -f docker-compose.production.yml down
```

### 清理资源

```bash
# 停止并删除所有容器
docker-compose -f docker-compose.production.yml down

# 删除所有相关镜像
docker rmi networktraffic-backend networktraffic-frontend

# 删除数据卷 (⚠️ 会删除数据库数据)
docker volume rm networktraffic_mysql_data_prod
```

---

## 🔍 故障排除

### 常见问题

#### 1. Docker 未运行
**错误信息:** `ERROR: Docker is not running or not installed!`

**解决方案:**
- 启动 Docker Desktop
- 等待 Docker 服务完全启动
- 重新运行部署脚本

#### 2. 端口被占用
**错误信息:** `Bind for 0.0.0.0:23456 failed: port is already allocated`

**解决方案:**
```bash
# 查看端口占用
netstat -ano | findstr :23456
netstat -ano | findstr :8000
netstat -ano | findstr :3307

# 停止占用端口的进程
taskkill /PID <进程ID> /F
```

#### 3. 前端无法连接后端
**症状:** 前端页面显示连接错误

**解决方案:**
1. 检查后端服务状态:
   ```bash
   docker-compose -f docker-compose.production.yml ps backend
   ```

2. 检查后端日志:
   ```bash
   docker-compose -f docker-compose.production.yml logs backend
   ```

3. 验证 API 端点:
   ```bash
   curl http://localhost:8000/api/health/
   ```

#### 4. 数据库连接失败
**错误信息:** `MySQL connection failed`

**解决方案:**
1. 检查 MySQL 容器状态:
   ```bash
   docker-compose -f docker-compose.production.yml ps mysql
   ```

2. 查看 MySQL 日志:
   ```bash
   docker-compose -f docker-compose.production.yml logs mysql
   ```

3. 重启 MySQL 服务:
   ```bash
   docker-compose -f docker-compose.production.yml restart mysql
   ```

#### 5. 构建失败
**错误信息:** `ERROR: Backend/Frontend Docker build failed!`

**解决方案:**
1. 清理 Docker 缓存:
   ```bash
   docker system prune -a
   ```

2. 重新构建:
   ```bash
   build-backend.bat
   build-frontend.bat
   ```

### 日志分析

#### 后端日志位置
- 容器日志: `docker logs network_traffic_backend_prod`
- 应用日志: `logs/` 目录

#### 前端日志位置
- 容器日志: `docker logs network_traffic_frontend_prod`
- 浏览器开发者工具控制台

#### 数据库日志位置
- 容器日志: `docker logs network_traffic_mysql_prod`

---

## ⚙️ 配置说明

### 环境变量配置 (.env)

项目会自动创建 `.env` 文件，包含以下配置:

```env
# 数据库配置
DB_NAME=NetworkTraffic
DB_USER=nwt_user
DB_PASSWORD=123456
DB_HOST=mysql
DB_PORT=3306
MYSQL_ROOT_PASSWORD=123456

# Django 配置
SECRET_KEY=network-traffic-production-secret-key-2024-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=http://localhost:3001,https://your-domain.com,https://www.your-domain.com

# 前端配置
VITE_API_BASE_URL=http://localhost:8000

# 部署配置
ENVIRONMENT=production
```

### 端口配置

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 23456 | Vue.js 应用 |
| 后端 | 8000 | Django API |
| 数据库 | 3307 | MySQL |

### 目录结构

```
NetworkTraffic/
├── HTTP/                    # Django 后端
│   ├── media/              # 媒体文件
│   ├── staticfiles/        # 静态文件
│   └── temp/               # 临时文件
├── UI/                     # Vue.js 前端
│   └── dist/               # 构建输出
├── mysql/                  # 数据库配置
├── nginx/                  # Nginx 配置
├── logs/                   # 日志文件
└── .env                    # 环境配置
```

---

## 📞 技术支持

### 获取帮助

1. **查看项目文档:**
   - `README.md` - 项目概述
   - `SCRIPTS_GUIDE.md` - 脚本使用指南

2. **检查日志文件:**
   - 应用日志: `logs/` 目录
   - Docker 日志: 使用 `docker logs` 命令

3. **常见问题:**
   - 确保 Docker Desktop 正在运行
   - 检查端口是否被占用
   - 验证网络连接

### 联系支持

如遇到无法解决的问题，请提供以下信息:
- 操作系统版本
- Docker 版本
- Node.js 版本
- 错误日志
- 复现步骤

---

## ✅ 部署验证清单

部署完成后，请验证以下项目:

- [ ] Docker Desktop 正在运行
- [ ] 所有服务容器正在运行
- [ ] 前端页面可以访问 (http://localhost:23456)
- [ ] 后端 API 可以访问 (http://localhost:8000)
- [ ] 可以正常登录 (admin/123456)
- [ ] 数据库连接正常
- [ ] 文件上传功能正常
- [ ] 聊天功能正常

---

## 📝 注意事项

1. **首次构建时间较长**：Docker镜像构建可能需要5-15分钟
2. **确保Docker Desktop运行**：所有脚本都需要Docker环境
3. **不要关闭构建窗口**：构建过程中请保持窗口打开
4. **模型服务**：当前版本中模型API服务未启动，相关功能会显示"服务暂时不可用"的提示

---

如有任何问题，欢迎联系项目维护者 👨‍💻👩‍💻

