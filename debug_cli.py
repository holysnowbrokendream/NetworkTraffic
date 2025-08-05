#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试版本的CLI工具
"""

import requests
import json
import sys

class DebugCLI:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.token = None
        self.headers = {
            'Content-Type': 'application/json'
        }
        print(f"🔍 初始化: base_url = {self.base_url}")
        print(f"🔍 初始化: token = {self.token}")
        print(f"🔍 初始化: headers = {self.headers}")
    
    def login(self, username, password):
        """用户登录"""
        print(f"🔍 登录开始: username = {username}")
        try:
            data = {
                'username': username,
                'password': password
            }
            print(f"🔍 发送登录请求: {data}")
            
            response = requests.post(f"{self.base_url}/login/", json=data, headers=self.headers)
            print(f"🔍 登录响应状态码: {response.status_code}")
            print(f"🔍 登录响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"🔍 解析响应: {result}")
                
                if result.get('status') == 'success':
                    self.token = result.get('token') or result.get('access')
                    print(f"🔍 获取token: {self.token}")
                    
                    if self.token:
                        self.headers['Authorization'] = f'Bearer {self.token}'
                        print(f"🔍 设置Authorization: {self.headers['Authorization']}")
                        print("✅ 登录成功！")
                        return True
                    else:
                        print("❌ 登录失败: 未获取到token")
                        return False
                else:
                    print(f"❌ 登录失败: {result}")
                    return False
            else:
                print(f"❌ 登录失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            return False
    
    def list_sessions(self):
        """列出聊天会话"""
        print(f"🔍 检查token: {self.token}")
        if not self.token:
            print("❌ 请先登录")
            return False
        
        try:
            print(f"🔍 发送请求到: {self.base_url}/api/modeltask/sessions/")
            print(f"🔍 使用headers: {self.headers}")
            
            response = requests.get(
                f"{self.base_url}/api/modeltask/sessions/",
                headers=self.headers
            )
            
            print(f"🔍 响应状态码: {response.status_code}")
            print(f"🔍 响应内容: {response.text}")
            
            if response.status_code == 200:
                sessions = response.json()
                if sessions:
                    print("📋 聊天会话列表:")
                    for session in sessions:
                        print(f"  - ID: {session.get('id')}, 创建时间: {session.get('created_at')}")
                else:
                    print("📋 暂无聊天会话")
                return True
            else:
                print(f"❌ 获取会话列表失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 获取会话列表失败: {e}")
            return False

def main():
    cli = DebugCLI()
    
    print("🔧 调试版CLI工具")
    print("输入 'login <用户名> <密码>' 进行登录")
    print("输入 'sessions' 查看会话")
    print("输入 'exit' 退出")
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if command == 'exit':
                print("👋 再见！")
                break
            elif command.startswith('login '):
                parts = command.split(' ', 2)
                if len(parts) >= 3:
                    cli.login(parts[1], parts[2])
                else:
                    print("❌ 格式: login <用户名> <密码>")
            elif command == 'sessions':
                cli.list_sessions()
            elif command:
                print("❌ 未知命令")
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main() 