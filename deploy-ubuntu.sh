#!/bin/bash

# Ubuntu部署脚本 - 网络流量分析系统
echo "🚀 开始部署网络流量分析系统..."

# 1. 检查Docker和Docker Compose
echo "📋 检查Docker环境..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 2. 创建环境变量文件
echo "🔧 配置环境变量..."
if [ ! -f .env ]; then
    echo "📝 创建.env文件..."
    cat > .env << EOF
# 数据库配置
DB_NAME=NetworkTraffic
DB_USER=nwt_user
DB_PASSWORD=123456
DB_HOST=mysql
DB_PORT=3306
MYSQL_ROOT_PASSWORD=123456

# Django配置
SECRET_KEY=django-insecure-dev-environment-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://localhost:3001,http://localhost:23456

# 前端配置
VITE_API_BASE_URL=http://localhost:8000

# 部署配置
ENVIRONMENT=production
EOF
    echo "✅ .env文件创建成功"
else
    echo "✅ .env文件已存在"
fi

# 3. 停止现有服务
echo "🛑 停止现有服务..."
docker-compose -f docker-compose.production.yml down

# 4. 清理容器和网络
echo "🧹 清理Docker环境..."
docker system prune -f

# 5. 重新构建和启动服务
echo "🔨 构建和启动服务..."
docker-compose -f docker-compose.production.yml up -d --build

# 6. 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 7. 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose.production.yml ps

# 8. 检查容器日志
echo "📋 检查后端日志..."
docker logs network_traffic_backend_prod --tail 20

echo "📋 检查MySQL日志..."
docker logs network_traffic_mysql_prod --tail 10

# 9. 执行数据库迁移
echo "🗄️ 执行数据库迁移..."
docker exec network_traffic_backend_prod python manage.py migrate

# 10. 测试API端点
echo "🧪 测试API端点..."
curl -X POST http://localhost:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}' \
  --connect-timeout 10

# 11. 显示访问信息
echo ""
echo "🎉 部署完成！"
echo "📱 前端访问地址: http://localhost:23456"
echo "🔧 后端API地址: http://localhost:8000"
echo "🗄️ 数据库端口: 3307"
echo ""
echo "🔍 故障排除命令:"
echo "  - 查看所有容器: docker ps -a"
echo "  - 查看后端日志: docker logs network_traffic_backend_prod"
echo "  - 查看前端日志: docker logs network_traffic_frontend_prod"
echo "  - 进入后端容器: docker exec -it network_traffic_backend_prod bash"
echo "  - 重启服务: docker-compose -f docker-compose.production.yml restart"
