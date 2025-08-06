#!/bin/bash

# ========================================
# 网络流量分析项目CLI工具启动脚本 (Linux)
# ========================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_success() { echo -e "${GREEN}$1${NC}"; }
print_error() { echo -e "${RED}$1${NC}"; }

# 检查Python环境
PYTHON_CMD=python3
if ! $PYTHON_CMD --version > /dev/null 2>&1; then
    print_error "❌ 未找到Python3，请确保Python3已安装并添加到PATH"
    exit 1
fi

# 检查requests库
if ! $PYTHON_CMD -c "import requests" > /dev/null 2>&1; then
    echo "📦 正在安装requests库..."
    $PYTHON_CMD -m pip install requests
fi

# 参数处理
if [ $# -eq 0 ]; then
    # 无参数，启动交互模式
    echo "🚀 启动交互模式..."
    $PYTHON_CMD cli_tool.py
    exit 0
fi

case $1 in
    interactive)
        echo "🚀 启动交互模式..."
        $PYTHON_CMD cli_tool.py
        ;;
    quick)
        echo "🚀 启动快速模式..."
        shift
        $PYTHON_CMD quick_cli.py "$@"
        ;;
    help)
        echo "📖 CLI工具帮助信息:"
        echo
        echo "用法:"
        echo "  ./cli_tool.sh                    - 启动交互模式"
        echo "  ./cli_tool.sh interactive        - 启动交互模式"
        echo "  ./cli_tool.sh quick analyze <文件路径>  - 快速分析PCAP文件"
        echo "  ./cli_tool.sh quick generate <提示词>   - 快速生成PCAP文件"
        echo "  ./cli_tool.sh help               - 显示此帮助信息"
        echo
        echo "📁 文件路径支持:"
        echo "  - 绝对路径: /path/to/file.pcap"
        echo "  - 相对路径: ./file.pcap"
        echo "  - 通配符: *.pcap (将使用第一个匹配的文件)"
        echo
        echo "💡 提示: 在Linux系统中，建议使用正斜杠(/)作为路径分隔符"
        ;;
    *)
        echo "🚀 执行命令: $@"
        $PYTHON_CMD cli_tool.py "$@"
        ;;
esac

print_success "👋 CLI工具执行完成"