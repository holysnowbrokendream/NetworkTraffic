#!/usr/bin/env python
"""
Django开发服务器启动脚本
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 检查是否在正确的目录
    if not Path('manage.py').exists():
        print("错误: 请在backend目录下运行此脚本")
        sys.exit(1)
    
    # 检查虚拟环境
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("警告: 建议在虚拟环境中运行")
        response = input("是否继续? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # 检查依赖
    try:
        import django
        print(f"Django版本: {django.get_version()}")
    except ImportError:
        print("错误: Django未安装，请运行: pip install -r requirements.txt")
        sys.exit(1)
    
    # 检查环境变量文件
    if not Path('.env').exists():
        print("警告: .env文件不存在，将使用默认配置")
        if Path('env.example').exists():
            print("请复制 env.example 到 .env 并配置环境变量")
    
    # 运行数据库迁移
    print("运行数据库迁移...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("数据库迁移完成")
    except subprocess.CalledProcessError as e:
        print(f"数据库迁移失败: {e}")
        sys.exit(1)
    
    # 启动开发服务器
    print("启动Django开发服务器...")
    print("服务器地址: http://127.0.0.1:8000")
    print("管理后台: http://127.0.0.1:8000/admin")
    print("按 Ctrl+C 停止服务器")
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n服务器已停止")

if __name__ == '__main__':
    main() 