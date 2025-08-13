#!/bin/bash

# ========================================
# 完整开发环境设置 (Linux)
# ========================================

set -e

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

echo "🚀 完整开发环境设置..."

echo
print_success "📝 步骤1: 设置环境变量..."
python3 setup_dev_env.py

echo
print_success "📝 步骤2: 初始化数据库..."
python3 init_database.py

echo
print_success "📝 步骤3: 运行数据库迁移..."
python3 manage.py migrate

echo
print_success "📝 步骤4: 收集静态文件..."
python3 manage.py collectstatic --noinput

echo
print_success "✅ 开发环境设置完成！"
echo

echo "📋 当前配置:"
echo "  数据库: localhost:3307/network_traffic"
echo "  用户名: nwt_user"
echo "  密码: 123456"
echo "  Django: DEBUG=True"
echo

echo "🚀 启动开发服务器:"
echo "  python manage.py runserver"
echo

echo "💡 其他常用命令:"
echo "  - 创建超级用户: python manage.py createsuperuser"
echo "  - 进入Django shell: python manage.py shell"
echo "  - 查看帮助: python manage.py help"
echo