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
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+, CentOS 7+
- **内存**: 8GB RAM
- **存储**: 20GB 可用空间
- **网络**: 稳定的互联网/内网连接

### 必需软件
- **Docker / Docker Desktop**: 版本 20.10+ 
- **Node.js**: 版本 18.0+ (用于前端构建)
- **Python3**: 版本 3.8+ (部分脚本和开发环境)

### 可选软件
- **Git**: 版本 2.30+ (用于代码管理，如果从仓库下载代码则需要)

---

## 🔧 环境准备

### Windows 环境

1. 安装 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. 安装 [Node.js](https://nodejs.org/)（LTS 18.x 或更高）
3. （可选）安装 [Git for Windows](https://git-scm.com/)
4. 验证安装：
   ```bash
   docker --version
   docker-compose --version
   node --version
   npm --version
   git --version
   ```

### Linux 环境（CentOS/Ubuntu/RHEL）

1. 安装 Docker
   ```bash
   # CentOS/RHEL
   sudo yum install -y yum-utils device-mapper-persistent-data lvm2
   sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
   sudo yum install -y docker-ce docker-ce-cli containerd.io
   sudo systemctl start docker && sudo systemctl enable docker
   sudo usermod -aG docker $USER
   
   # Ubuntu
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io
   sudo systemctl start docker && sudo systemctl enable docker
   sudo usermod -aG docker $USER
   ```
   
2. 安装 Docker Compose
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   docker-compose --version
   ```
   
3. 安装 Node.js
   ```bash
   # CentOS/RHEL
   curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
   sudo yum install -y nodejs
   
   # Ubuntu
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   sudo apt-get install -y nodejs
   node --version
   npm --version
   ```
   
4. 安装 Python3
   ```bash
   # CentOS/RHEL
   sudo yum install -y python3 python3-pip
   
   # Ubuntu
   sudo apt-get install -y python3 python3-pip
   python3 --version
   ```
   
5. （可选）安装 Git
   ```bash
   sudo yum install -y git   # CentOS/RHEL
   sudo apt-get install -y git   # Ubuntu
   git --version
   ```

---

## 🚀 快速部署

### Windows 版本

1. **一键部署**
   ```bash
   deploy-all.bat
   ```
2. **分步部署**
   - 构建后端：`build-backend.bat`
   - 构建前端：`build-frontend.bat`
   - 启动服务：`start-services.bat`
3. **内网部署**
   - 网络访问配置：`cd HTTP && configure_network_access.bat`
   - 防火墙配置：`cd HTTP && configure_firewall.bat`

### Linux 版本

1. **赋予脚本执行权限**
   ```bash
   chmod +x deploy-all.sh build-backend.sh build-frontend.sh start-services.sh
   chmod +x HTTP/configure_firewall.sh HTTP/configure_network_access.sh
   ```
2. **一键部署**
   ```bash
   ./deploy-all.sh
   ```
3. **分步部署**
   - 构建后端：`./build-backend.sh`
   - 构建前端：`./build-frontend.sh`
   - 启动服务：`./start-services.sh`
4. **内网部署**
   - 网络访问配置：`cd HTTP && ./configure_network_access.sh`
   - 防火墙配置：`cd HTTP && sudo ./configure_firewall.sh`

---

### 内网部署

## 🛠️ 脚本使用指南

### Windows 版本

- **deploy-all.bat**：一键完整部署脚本
- **build-backend.bat**：构建后端 Docker 镜像
- **build-frontend.bat**：构建前端应用和镜像
- **start-services.bat**：启动所有服务
- **HTTP/configure_firewall.bat**：配置防火墙规则
- **HTTP/configure_network_access.bat**：配置网络访问
- **setup_dev_env.bat**：开发环境变量设置
- **setup_dev_complete.bat**：完整开发环境设置
- **cli_tool.bat**：CLI 工具启动脚本

### Linux 版本

- **deploy-all.sh**：一键完整部署脚本
- **build-backend.sh**：构建后端 Docker 镜像
- **build-frontend.sh**：构建前端应用和镜像
- **start-services.sh**：启动所有服务
- **HTTP/configure_firewall.sh**：配置防火墙规则
- **HTTP/configure_network_access.sh**：配置网络访问
- **setup_dev_env.sh**：开发环境变量设置
- **setup_dev_complete.sh**：完整开发环境设置
- **cli_tool.sh**：CLI 工具启动脚本

---

## 🛠️ 服务管理

### Windows/Linux 版本

- 查看服务状态：
  ```bash
  docker-compose -f docker-compose.production.yml ps
  ```
- 查看服务日志：
  ```bash
  docker-compose -f docker-compose.production.yml logs -f
  docker-compose -f docker-compose.production.yml logs -f backend
  docker-compose -f docker-compose.production.yml logs -f frontend
  docker-compose -f docker-compose.production.yml logs -f mysql
  ```
- 重启服务：
  ```bash
  docker-compose -f docker-compose.production.yml restart
  docker-compose -f docker-compose.production.yml restart backend
  docker-compose -f docker-compose.production.yml restart frontend
  ```
- 停止服务：
  ```bash
  docker-compose -f docker-compose.production.yml down
  ```
- 清理资源：
  ```bash
  docker-compose -f docker-compose.production.yml down
  docker rmi networktraffic-backend networktraffic-frontend
  docker volume rm networktraffic_mysql_data_prod
  ```
  
- 推荐使用脚本进行服务启动、停止、重启。
- 日志、端口、资源清理等命令双系统兼容。

---

## 🔍 故障排除

### Linux 常见问题

- **权限问题**：
  ```bash
  newgrp docker
  # 或 sudo reboot
  ```
- **端口被占用**：
  ```bash
  sudo netstat -tulpn | grep :23456
  sudo netstat -tulpn | grep :8000
  sudo kill -9 <进程ID>
  ```
- **SELinux 问题**：
  ```bash
  sudo setenforce 0
  sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
  ```
- **内存不足**：
  ```bash
  sudo fallocate -l 2G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
  ```
- **日志查看**：
  ```bash
  docker-compose -f docker-compose.production.yml logs -f
  docker-compose -f docker-compose.production.yml logs -f backend
  docker-compose -f docker-compose.production.yml logs -f frontend
  docker-compose -f docker-compose.production.yml logs -f mysql
  ```

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
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*,your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=http://localhost:3001,http://localhost:23456,http://127.0.0.1:23456,http://0.0.0.0:23456,http://*:23456,https://your-domain.com,https://www.your-domain.com

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

1. **查看项目文档:**
   - `README.md` - 项目概述、部署说明
2. **检查日志文件:**
   - 应用日志: `logs/` 目录
   - Docker 日志: 使用 `docker logs` 命令
3. **常见问题:**
   - 确保 Docker 正常运行
   - 检查端口是否被占用
   - 验证网络连接和防火墙设置

如遇到无法解决的问题，请提供：操作系统版本、Docker/Node.js 版本、错误日志、复现步骤、网络环境等信息。

---

## ✅ 部署验证清单

部署完成后，请验证以下项目:

- [ ] Docker 服务正在运行
- [ ] 所有服务容器正在运行
- [ ] 前端页面可以访问 (http://localhost:23456)
- [ ] 后端 API 可以访问 (http://localhost:8000)
- [ ] 可以正常登录 (admin/123456)
- [ ] 数据库连接正常
- [ ] 文件上传功能正常
- [ ] 聊天功能正常
- [ ] 防火墙规则已配置 (内网部署)
- [ ] 网络访问正常 (内网部署)

---

## 📝 注意事项

1. **首次构建时间较长**：Docker 镜像构建可能需要 5-15 分钟
2. **确保 Docker 服务运行**：所有脚本都需要 Docker 环境
3. **不要关闭终端/窗口**：构建过程中请保持窗口打开
4. **权限问题**：Linux 某些操作需要 root 权限
5. **网络配置**：内网部署需要额外的网络和防火墙配置
6. **日志查看**：推荐使用 `docker-compose logs` 查看详细日志

---

如有任何问题，欢迎联系项目维护者 👨‍💻👩‍💻

