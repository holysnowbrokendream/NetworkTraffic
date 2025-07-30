#!/usr/bin/env python3
"""
将env.example的内容应用到虚拟环境
使用方法: python setup_dev_env.py
"""

import os
import sys
from pathlib import Path

def setup_dev_environment():
    """设置开发环境变量"""
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    http_dir = Path(__file__).parent
    
    # 读取env.example文件
    env_example_path = project_root / "env.example"
    if not env_example_path.exists():
        print("❌ env.example 文件不存在")
        return False
    
    # 读取环境变量内容
    with open(env_example_path, 'r', encoding='utf-8') as f:
        env_content = f.read()
    
    # 创建HTTP目录下的.env文件
    env_file_path = http_dir / ".env"
    
    # 写入环境变量到HTTP/.env
    with open(env_file_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ 环境变量已写入到 HTTP/.env")
    print(f"📁 文件位置: {env_file_path}")
    
    # 显示配置信息
    print("\n📋 当前配置:")
    print("数据库配置:")
    print("  - 数据库名: network_traffic")
    print("  - 用户名: root")
    print("  - 密码: 123456")
    print("  - 主机: localhost")
    print("  - 端口: 3306")
    print("\nDjango配置:")
    print("  - DEBUG: True")
    print("  - 环境: development")
    
    return True

def check_mysql_connection():
    """检查MySQL连接"""
    try:
        import mysql.connector
        from decouple import config
        
        # 读取环境变量
        db_config = {
            'host': config('DB_HOST', default='localhost'),
            'user': config('DB_USER', default='root'),
            'password': config('DB_PASSWORD', default='123456'),
            'port': config('DB_PORT', default=3306, cast=int)
        }
        
        # 尝试连接
        conn = mysql.connector.connect(**db_config)
        print("✅ MySQL连接成功")
        conn.close()
        return True
        
    except ImportError:
        print("⚠️  mysql-connector-python 未安装，跳过连接测试")
        print("   安装命令: pip install mysql-connector-python")
        return False
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        print("请确保MySQL服务正在运行")
        return False

def main():
    """主函数"""
    print("🚀 设置开发环境变量...")
    
    # 设置环境变量
    if setup_dev_environment():
        print("\n🔍 检查MySQL连接...")
        check_mysql_connection()
        
        print("\n📝 下一步操作:")
        print("1. 确保MySQL服务正在运行")
        print("2. 创建数据库: CREATE DATABASE network_traffic;")
        print("3. 运行数据库迁移: python manage.py migrate")
        print("4. 启动开发服务器: python manage.py runserver")
        
        print("\n💡 提示:")
        print("- 如果MySQL未安装，请先安装MySQL")
        print("- 如果连接失败，请检查MySQL服务状态")
        print("- 可以使用 'mysql -u root -p' 命令测试连接")
    else:
        print("❌ 环境设置失败")

if __name__ == "__main__":
    main() 