#!/bin/bash

# ========================================
# Docker权限修复脚本
# ========================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "========================================"
echo "Docker权限修复脚本"
echo "========================================"

# 检查Docker是否安装
print_status "检查Docker安装状态..."
if ! command -v docker &> /dev/null; then
    print_error "Docker未安装，请先安装Docker"
    exit 1
fi
print_success "Docker已安装: $(docker --version)"

# 检查Docker服务状态
print_status "检查Docker服务状态..."
if sudo systemctl is-active --quiet docker; then
    print_success "Docker服务正在运行"
else
    print_error "Docker服务未运行，正在启动..."
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# 检查当前用户是否在docker组中
print_status "检查用户权限..."
if groups $USER | grep -q docker; then
    print_success "用户已在docker组中"
else
    print_warning "用户不在docker组中，正在添加..."
    sudo usermod -aG docker $USER
    print_success "用户已添加到docker组"
fi

# 检查Docker socket权限
print_status "检查Docker socket权限..."
if [ -S /var/run/docker.sock ]; then
    SOCKET_PERMS=$(stat -c "%a" /var/run/docker.sock)
    SOCKET_GROUP=$(stat -c "%G" /var/run/docker.sock)
    print_status "Docker socket权限: $SOCKET_PERMS, 组: $SOCKET_GROUP"
    
    if [ "$SOCKET_GROUP" = "docker" ]; then
        print_success "Docker socket组权限正确"
    else
        print_warning "Docker socket组权限可能有问题"
    fi
else
    print_error "Docker socket不存在"
    exit 1
fi

# 尝试重新加载组权限
print_status "重新加载组权限..."
newgrp docker << EONG
print_status "在新的组环境中测试Docker权限..."
if docker ps &> /dev/null; then
    print_success "Docker权限正常"
else
    print_error "Docker权限仍然有问题"
fi
EONG

# 提供解决方案选项
echo
echo "========================================"
echo "权限修复完成！"
echo "========================================"
echo
echo "如果权限问题仍然存在，请尝试以下方法："
echo
echo "方法1: 重新登录"
echo "   logout"
echo "   然后重新登录"
echo
echo "方法2: 重启系统"
echo "   sudo reboot"
echo
echo "方法3: 使用sudo运行Docker命令"
echo "   sudo docker-compose -f docker-compose.production.yml build backend"
echo
echo "方法4: 临时切换到root用户"
echo "   sudo su -"
echo "   docker-compose -f docker-compose.production.yml build backend"
echo
echo "验证Docker权限:"
echo "   docker ps"
echo "   docker info" 