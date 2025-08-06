#!/bin/bash

# ========================================
# 设置开发环境变量 (Linux)
# ========================================

set -e

# 彩色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_success() { echo -e "${GREEN}$1${NC}"; }
print_error() { echo -e "${RED}$1${NC}"; }

# 激活虚拟环境
if [ -d ".venv" ]; then
    source .venv/bin/activate
    print_success "已激活虚拟环境 .venv"
else
    print_error "未找到 .venv 虚拟环境，请先创建虚拟环境 (python3 -m venv .venv)"
    exit 1
fi

echo "🚀 设置开发环境变量..."

# 运行Python脚本设置环境变量
python3 setup_dev_env.py

# 检查是否成功创建.env文件
if [ -f .env ]; then
    echo
    print_success "✅ 环境变量设置完成！"
    echo
    echo "📋 当前配置:"
    echo "  数据库: localhost:3306"
    echo "  用户名: nwt_user"
    echo "  密码: 123456"
    echo "  数据库名: network_traffic"
    echo
    echo "📝 下一步操作:"
    echo "  1. 确保MySQL服务正在运行"
    echo "  2. 创建数据库: CREATE DATABASE network_traffic;"
    echo "  3. 运行迁移: python manage.py migrate"
    echo "  4. 启动服务器: python manage.py runserver"
    echo
else
    print_error "❌ 环境变量设置失败"
    exit 1
fi