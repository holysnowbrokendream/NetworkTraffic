# Docker镜像导出包使用说明

## 文件说明

本目录包含预构建的Docker镜像，可直接导入使用，无需重新构建。

### 镜像文件
- `networktraffic-backend.tar` - 后端Django API镜像
- `networktraffic-frontend.tar` - 前端Vue.js应用镜像  
- `mysql-8.0.tar` - MySQL 8.0数据库镜像

### 脚本文件
- `import-images.bat` - Windows导入脚本
- `import-images.sh` - Linux/Mac导入脚本
- `images-setup.bat` - Windows环境配置脚本
- `images-setup.sh` - Linux环境配置脚本
- `start-services-images.bat` - Windows服务启动脚本
- `start-services-images.sh` - Linux服务启动脚本

## 使用方法

### Windows用户
1. 确保Docker Desktop正在运行
2. 双击运行 `import-images.bat`
3. 等待镜像导入完成
4. 运行 `images-setup.bat` 配置环境
5. 运行 `start-services-images.bat` 启动服务

### Linux/Mac用户
1. 确保Docker服务正在运行
2. 给脚本添加执行权限：`chmod +x import-images.sh images-setup.sh start-services-images.sh`
3. 运行导入脚本：`./import-images.sh`
4. 等待镜像导入完成
5. 运行 `./images-setup.sh` 配置环境
6. 运行 `./start-services-images.sh` 启动服务

## 注意事项

- 导入镜像需要几分钟时间，请耐心等待
- 确保有足够的磁盘空间（约2-3GB）
- 导入完成后，镜像会出现在 `docker images` 列表中
- 环境配置脚本会自动检测主机IP并生成配置文件
- 首次启动服务时，数据库初始化可能需要额外时间

## 访问地址

服务启动成功后，可通过以下地址访问：
- 前端应用：http://localhost:23456
- 后端API：http://localhost:8000
- 管理界面：http://localhost:8000/admin/

## 测试账户

- 管理员：admin/123456
- 测试用户：yang/123456

## 目录结构

```
DockerImages/
├── networktraffic-backend.tar    # 后端镜像
├── networktraffic-frontend.tar   # 前端镜像
├── mysql-8.0.tar                # MySQL镜像
├── import-images.bat            # Windows导入脚本
├── import-images.sh             # Linux导入脚本
├── images-setup.bat             # Windows环境配置脚本
├── images-setup.sh              # Linux环境配置脚本
├── start-services-images.bat    # Windows服务启动脚本
├── start-services-images.sh     # Linux服务启动脚本
└── README.md                    # 使用说明
```

## 故障排除

### 常见问题

1. **镜像导入失败**
   - 检查Docker是否正在运行
   - 确保有足够的磁盘空间
   - 验证tar文件是否完整

2. **服务启动失败**
   - 检查镜像是否成功导入：`docker images`
   - 查看容器日志：`docker logs <container_name>`
   - 确保端口未被占用

3. **数据库连接失败**
   - 等待MySQL容器完全启动
   - 检查数据库配置是否正确
   - 查看MySQL容器状态：`docker ps`

### 获取帮助

如果遇到问题，请：
1. 查看容器日志
2. 检查Docker服务状态
3. 参考项目根目录的部署文档
