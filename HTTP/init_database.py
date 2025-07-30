#!/usr/bin/env python3
"""
数据库初始化脚本
使用方法: python init_database.py
"""

import mysql.connector
from mysql.connector import Error
from decouple import config

def create_database():
    """创建数据库"""
    try:
        # 连接MySQL（不指定数据库）
        connection = mysql.connector.connect(
            host=config('DB_HOST', default='localhost'),
            user=config('DB_USER', default='root'),
            password=config('DB_PASSWORD', default='123456'),
            port=config('DB_PORT', default=3306, cast=int)
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 创建数据库
            db_name = config('DB_NAME', default='network_traffic')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"✅ 数据库 '{db_name}' 创建成功")
            
            # 切换到新创建的数据库
            cursor.execute(f"USE {db_name}")
            print(f"✅ 已切换到数据库 '{db_name}'")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ 数据库创建失败: {e}")
        return False

def check_database_exists():
    """检查数据库是否存在"""
    try:
        connection = mysql.connector.connect(
            host=config('DB_HOST', default='localhost'),
            user=config('DB_USER', default='root'),
            password=config('DB_PASSWORD', default='123456'),
            port=config('DB_PORT', default=3306, cast=int)
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 检查数据库是否存在
            db_name = config('DB_NAME', default='network_traffic')
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if db_name in databases:
                print(f"✅ 数据库 '{db_name}' 已存在")
                return True
            else:
                print(f"❌ 数据库 '{db_name}' 不存在")
                return False
                
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ 检查数据库失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 初始化数据库...")
    
    # 检查数据库是否存在
    if not check_database_exists():
        print("\n📝 创建数据库...")
        if create_database():
            print("✅ 数据库初始化完成")
        else:
            print("❌ 数据库初始化失败")
            return
    
    print("\n📋 数据库配置:")
    print(f"  - 主机: {config('DB_HOST', default='localhost')}")
    print(f"  - 端口: {config('DB_PORT', default=3306)}")
    print(f"  - 用户: {config('DB_USER', default='root')}")
    print(f"  - 数据库: {config('DB_NAME', default='network_traffic')}")
    
    print("\n📝 下一步操作:")
    print("1. 运行数据库迁移: python manage.py migrate")
    print("2. 创建超级用户: python manage.py createsuperuser")
    print("3. 启动开发服务器: python manage.py runserver")

if __name__ == "__main__":
    main() 