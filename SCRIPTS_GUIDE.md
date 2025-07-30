# 网络流量分析系统 - 脚本使用指南

## 可用的部署脚本

### 1. 完整部署脚本
- **`deploy-all.bat`** - 一键完整部署脚本
  - 构建后端 (Django API)
  - 构建前端 (Vue.js)
  - 启动所有服务 (MySQL, Backend, Frontend)
  - 创建默认用户账户
  - 测试API功能

### 2. 分步构建脚本
- **`build-backend.bat`** - 构建后端Docker镜像
- **`build-frontend.bat`** - 构建前端应用和Docker镜像

### 3. 服务管理脚本
- **`start-services.bat`** - 启动所有服务
  - 按顺序启动 MySQL → Backend → Frontend
  - 包含健康检查和等待机制
  - 创建默认用户账户
  - 测试API功能

## 使用建议

### 首次部署
```bash
# 推荐使用完整部署脚本
.\deploy-all.bat
```

### 重新构建
```bash
# 如果修改了代码，需要重新构建
.\build-backend.bat
.\build-frontend.bat
.\start-services.bat
```

### 仅重启服务
```bash
# 如果只是重启服务，不需要重新构建
.\start-services.bat
```

## 访问地址

部署完成后，可以通过以下地址访问：

- **前端应用**: http://localhost:23456
- **后端API**: http://localhost:8000
- **管理界面**: http://localhost:8000/admin/
- **数据库**: localhost:3307

## 默认用户账户

- **管理员**: admin / 123456
- **测试用户**: yang / 123456

## 故障排除

### 端口冲突
如果遇到端口冲突，检查：
```bash
netstat -ano | findstr :23456
netstat -ano | findstr :8000
netstat -ano | findstr :3307
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose -f docker-compose.production.yml logs -f

# 查看特定服务日志
docker-compose -f docker-compose.production.yml logs -f backend
docker-compose -f docker-compose.production.yml logs -f frontend
docker-compose -f docker-compose.production.yml logs -f mysql
```

### 停止服务
```bash
docker-compose -f docker-compose.production.yml down
```

### 重启服务
```bash
docker-compose -f docker-compose.production.yml restart
```

## 注意事项

1. **首次构建时间较长**：Docker镜像构建可能需要5-15分钟
2. **确保Docker Desktop运行**：所有脚本都需要Docker环境
3. **不要关闭构建窗口**：构建过程中请保持窗口打开
4. **模型服务**：当前版本中模型API服务未启动，相关功能会显示"服务暂时不可用"的提示

## 已删除的脚本

以下脚本已被删除，不再使用：
- `production-deploy.bat` - 旧的单文件部署脚本
- `production-manager.bat` - 旧的管理脚本
- `deploy.bat` - 开发环境脚本
- `simple-test.bat` - 测试脚本
- `test-npm.bat` - npm测试脚本 