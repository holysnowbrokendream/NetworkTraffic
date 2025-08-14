#!/bin/bash

# ========================================
# Docker安装脚本（使用指定镜像源）
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
echo "Docker安装脚本（使用指定镜像源）"
echo "========================================"

# 检查系统版本
print_status "检查系统版本..."
if ! command -v lsb_release &> /dev/null; then
    print_error "lsb_release命令不可用，请安装lsb-release包"
    sudo apt install -y lsb-release
fi

UBUNTU_VERSION=$(lsb_release -cs)
print_success "检测到Ubuntu版本: $UBUNTU_VERSION"

# 1. 清理旧配置
print_status "清理旧的Docker配置..."
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /usr/share/keyrings/docker-archive-keyring.gpg
print_success "旧配置已清理"

# 2. 安装必要的包
print_status "安装必要的包..."
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# 3. 使用指定镜像源添加GPG密钥
print_status "使用指定镜像源添加GPG密钥..."
if curl -fsSL https://docker.xuanyuan.me/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg; then
    print_success "GPG密钥添加成功"
else
    print_error "GPG密钥添加失败，请检查网络连接"
    exit 1
fi

# 4. 添加指定镜像源仓库
print_status "添加指定镜像源仓库..."
REPO_LINE="deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://docker.xuanyuan.me/linux/ubuntu $UBUNTU_VERSION stable"
echo "$REPO_LINE" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
print_success "指定镜像源仓库已添加"

# 5. 更新包索引
print_status "更新包索引..."
sudo apt update

# 6. 验证Docker包是否可用
print_status "验证Docker包可用性..."
if apt list docker-ce 2>/dev/null | grep -q "docker-ce"; then
    print_success "Docker包现在可用"
else
    print_error "Docker包仍然不可用，请检查网络连接"
    echo "尝试手动检查:"
    echo "apt list docker-ce"
    exit 1
fi

# 7. 安装Docker
print_status "安装Docker..."
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 8. 启动Docker服务
print_status "启动Docker服务..."
sudo systemctl start docker
sudo systemctl enable docker

# 9. 配置用户权限
print_status "配置用户权限..."
sudo usermod -aG docker $USER

# 10. 配置Docker镜像源
print_status "配置Docker镜像源..."
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://docker.xuanyuan.me"
  ],
  "insecure-registries": [],
  "debug": false,
  "experimental": false
}
EOF

# 重启Docker服务以应用镜像源配置
sudo systemctl restart docker
print_success "Docker镜像源配置完成"

# 11. 验证安装
print_status "验证Docker安装..."
if docker --version &> /dev/null; then
    print_success "Docker安装成功: $(docker --version)"
else
    print_error "Docker安装失败"
    exit 1
fi

# 12. 测试Docker功能
print_status "测试Docker功能..."
if sudo docker run hello-world &> /dev/null; then
    print_success "Docker功能正常"
else
    print_warning "Docker功能测试失败，但安装可能成功"
fi

# 13. 验证镜像源配置
print_status "验证镜像源配置..."
if docker info | grep -q "docker.xuanyuan.me"; then
    print_success "镜像源配置成功"
else
    print_warning "镜像源配置可能未生效，请检查网络连接"
fi

echo
echo "========================================"
print_success "Docker安装完成！"
echo "========================================"
echo "使用的镜像源: https://docker.xuanyuan.me"
echo
echo "重要提示："
echo "1. 请重新登录或重启系统以应用docker组权限"
echo "2. 重新登录后，您可以使用 'docker' 命令而无需sudo"
echo "3. 验证命令: docker --version"
echo "4. 测试命令: docker run hello-world"
echo "5. 验证镜像源: docker info | grep -A 5 'Registry Mirrors'"
echo
echo "如果遇到权限问题，请运行:"
echo "newgrp docker"
echo "或重启系统" 