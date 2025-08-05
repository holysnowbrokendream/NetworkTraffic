#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络流量分析项目CLI工具
提供用户管理、模型服务和聊天会话管理功能
"""

import requests
import json
import os
import glob
import argparse
import getpass
from pathlib import Path

class NetworkTrafficCLI:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.token = None
        self.headers = {
            'Content-Type': 'application/json'
        }
        # 尝试从文件加载token
        self.load_token()
    
    def save_token(self):
        """保存token到文件"""
        try:
            with open('.cli_token', 'w') as f:
                f.write(self.token or '')
            print(f"🔍 已保存token到文件")
        except Exception as e:
            print(f"⚠️ 保存token失败: {e}")
    
    def load_token(self):
        """从文件加载token"""
        try:
            if os.path.exists('.cli_token'):
                with open('.cli_token', 'r') as f:
                    token = f.read().strip()
                    if token:
                        self.token = token
                        self.headers['Authorization'] = f'Bearer {self.token}'
                        print("🔍 已加载保存的token")
        except Exception as e:
            print(f"⚠️ 加载token失败: {e}")
    
    def clear_token(self):
        """清除保存的token"""
        try:
            if os.path.exists('.cli_token'):
                os.remove('.cli_token')
                print("🔍 已清除保存的token")
        except Exception as e:
            print(f"⚠️ 清除token失败: {e}")
    
    def login(self, username, password):
        """用户登录"""
        try:
            data = {
                'username': username,
                'password': password
            }
            response = requests.post(f"{self.base_url}/login/", json=data, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    self.token = result.get('token') or result.get('access')
                    if self.token:
                        self.headers['Authorization'] = f'Bearer {self.token}'
                        self.save_token()  # 保存token到文件
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
    
    def register(self, username, password, email):
        """用户注册"""
        try:
            data = {
                'username': username,
                'password': password,
                'email': email
            }
            response = requests.post(f"{self.base_url}/register/", json=data, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    print("✅ 注册成功！")
                    return True
                else:
                    print(f"❌ 注册失败: {result}")
                    return False
            else:
                print(f"❌ 注册失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 注册失败: {e}")
            return False
    
    def logout(self):
        """退出登录"""
        self.token = None
        self.headers.pop('Authorization', None)
        self.clear_token()  # 清除保存的token
        print("✅ 已退出登录")
    
    def analyze_pcap(self, file_path):
        """分析PCAP文件"""
        if not self.token:
            print("❌ 请先登录")
            return False
        
        try:
            # 处理文件路径
            if '*' in file_path:
                files = glob.glob(file_path)
                if not files:
                    print(f"❌ 未找到匹配的文件: {file_path}")
                    return False
                file_path = files[0]
                print(f"📁 使用文件: {file_path}")
            
            # 转换为绝对路径
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
            
            if not os.path.exists(file_path):
                print(f"❌ 文件不存在: {file_path}")
                return False
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.base_url}/api/modeltask/analyze/",
                    files=files,
                    headers={'Authorization': f'Bearer {self.token}'}
                )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 分析完成！")
                print(f"📊 分析结果: {result}")
                return True
            else:
                print(f"❌ 分析失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            return False
    
    def generate_pcap(self, prompt):
        """生成PCAP文件"""
        if not self.token:
            print("❌ 请先登录")
            return False
        
        try:
            data = {'prompt': prompt}
            response = requests.post(
                f"{self.base_url}/api/modeltask/generate/",
                json=data,
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    file_url = result.get('file_url')
                    if file_url:
                        # 下载文件
                        file_response = requests.get(file_url)
                        if file_response.status_code == 200:
                            filename = f"generated_{prompt[:20]}.pcap"
                            with open(filename, 'wb') as f:
                                f.write(file_response.content)
                            print(f"✅ 生成完成！文件保存为: {os.path.abspath(filename)}")
                            return True
                        else:
                            print("❌ 下载生成文件失败")
                            return False
                    else:
                        print("❌ 生成失败: 未返回文件URL")
                        return False
                else:
                    print(f"❌ 生成失败: {result}")
                    return False
            else:
                print(f"❌ 生成失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return False
    
    def list_sessions(self):
        """列出聊天会话"""
        if not self.token:
            print("❌ 请先登录")
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/api/modeltask/sessions/",
                headers=self.headers
            )
            
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
    
    def view_session(self, session_id):
        """查看会话详情"""
        if not self.token:
            print("❌ 请先登录")
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/api/modeltask/sessions/{session_id}/",
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            if response.status_code == 200:
                session = response.json()
                print(f"📋 会话详情 (ID: {session_id}):")
                print(f"  创建时间: {session.get('created_at')}")
                messages = session.get('messages', [])
                if messages:
                    print("  消息列表:")
                    for msg in messages:
                        print(f"    - {msg.get('role')}: {msg.get('content')}")
                else:
                    print("  暂无消息")
                return True
            else:
                print(f"❌ 获取会话详情失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 获取会话详情失败: {e}")
            return False
    
    def create_session(self):
        """创建新会话"""
        if not self.token:
            print("❌ 请先登录")
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/api/modeltask/sessions/",
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            if response.status_code == 201:
                session = response.json()
                print(f"✅ 创建会话成功！ID: {session.get('id')}")
                return True
            else:
                print(f"❌ 创建会话失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 创建会话失败: {e}")
            return False
    
    def send_message(self, session_id, content):
        """发送消息"""
        if not self.token:
            print("❌ 请先登录")
            return False
        
        try:
            data = {'content': content}
            response = requests.post(
                f"{self.base_url}/api/modeltask/sessions/{session_id}/messages/",
                json=data,
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            if response.status_code == 201:
                print("✅ 消息发送成功！")
                return True
            else:
                print(f"❌ 发送消息失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 发送消息失败: {e}")
            return False
    
    def send_message_file(self, session_id, file_path):
        """发送带文件的消息"""
        if not self.token:
            print("❌ 请先登录")
            return False
        
        try:
            # 处理文件路径
            if '*' in file_path:
                files = glob.glob(file_path)
                if not files:
                    print(f"❌ 未找到匹配的文件: {file_path}")
                    return False
                file_path = files[0]
                print(f"📁 使用文件: {file_path}")
            
            # 转换为绝对路径
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
            
            if not os.path.exists(file_path):
                print(f"❌ 文件不存在: {file_path}")
                return False
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.base_url}/api/modeltask/sessions/{session_id}/messages/",
                    files=files,
                    headers={'Authorization': f'Bearer {self.token}'}
                )
            
            if response.status_code == 201:
                print("✅ 文件消息发送成功！")
                return True
            else:
                print(f"❌ 发送文件消息失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 发送文件消息失败: {e}")
            return False
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🔧 网络流量分析项目CLI工具

📋 可用命令:
  login <用户名> <密码>          - 用户登录
  register <用户名> <密码> <邮箱> - 用户注册
  logout                        - 退出登录
  
  analyze <文件路径>             - 分析PCAP文件
  generate <提示词>              - 生成PCAP文件
  
  sessions                      - 列出聊天会话
  view <会话ID>                 - 查看会话详情
  create                        - 创建新会话
  message <会话ID> <内容>        - 发送消息
  message-file <会话ID> <文件路径> - 发送带文件的消息
  
  help                          - 显示此帮助信息
  exit                          - 退出程序

📁 文件路径支持:
  - 绝对路径: C:/path/to/file.pcap
  - 相对路径: ./file.pcap
  - 通配符: *.pcap (将使用第一个匹配的文件)
  
💡 提示: 在Windows系统中，建议使用正斜杠(/)而不是反斜杠(\\)来避免路径问题
        """
        print(help_text)

def main():
    cli = NetworkTrafficCLI()
    
    if len(sys.argv) > 1:
        # 命令行模式
        command = sys.argv[1]
        
        if command == 'login' and len(sys.argv) >= 4:
            cli.login(sys.argv[2], sys.argv[3])
        elif command == 'register' and len(sys.argv) >= 5:
            cli.register(sys.argv[2], sys.argv[3], sys.argv[4])
        elif command == 'logout':
            cli.logout()
        elif command == 'analyze' and len(sys.argv) >= 3:
            cli.analyze_pcap(sys.argv[2])
        elif command == 'generate' and len(sys.argv) >= 3:
            cli.generate_pcap(sys.argv[2])
        elif command == 'sessions':
            cli.list_sessions()
        elif command == 'view' and len(sys.argv) >= 3:
            cli.view_session(sys.argv[2])
        elif command == 'create':
            cli.create_session()
        elif command == 'message' and len(sys.argv) >= 4:
            cli.send_message(sys.argv[2], sys.argv[3])
        elif command == 'message-file' and len(sys.argv) >= 4:
            cli.send_message_file(sys.argv[2], sys.argv[3])
        elif command == 'help':
            cli.show_help()
        else:
            print("❌ 命令格式错误，使用 'help' 查看帮助")
    else:
        # 交互模式
        print("🔧 网络流量分析项目CLI工具")
        print("输入 'help' 查看帮助，'exit' 退出程序")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if command == 'exit':
                    print("👋 再见！")
                    break
                elif command == 'help':
                    cli.show_help()
                elif command.startswith('login '):
                    parts = command.split(' ', 2)
                    if len(parts) >= 3:
                        cli.login(parts[1], parts[2])
                    else:
                        print("❌ 格式: login <用户名> <密码>")
                elif command.startswith('register '):
                    parts = command.split(' ', 3)
                    if len(parts) >= 4:
                        cli.register(parts[1], parts[2], parts[3])
                    else:
                        print("❌ 格式: register <用户名> <密码> <邮箱>")
                elif command == 'logout':
                    cli.logout()
                elif command.startswith('analyze '):
                    file_path = command[8:].strip()
                    if file_path:
                        cli.analyze_pcap(file_path)
                    else:
                        print("❌ 格式: analyze <文件路径>")
                elif command.startswith('generate '):
                    prompt = command[9:].strip()
                    if prompt:
                        cli.generate_pcap(prompt)
                    else:
                        print("❌ 格式: generate <提示词>")
                elif command == 'sessions':
                    cli.list_sessions()
                elif command.startswith('view '):
                    session_id = command[5:].strip()
                    if session_id:
                        cli.view_session(session_id)
                    else:
                        print("❌ 格式: view <会话ID>")
                elif command == 'create':
                    cli.create_session()
                elif command.startswith('message '):
                    parts = command.split(' ', 2)
                    if len(parts) >= 3:
                        cli.send_message(parts[1], parts[2])
                    else:
                        print("❌ 格式: message <会话ID> <内容>")
                elif command.startswith('message-file '):
                    parts = command.split(' ', 2)
                    if len(parts) >= 3:
                        cli.send_message_file(parts[1], parts[2])
                    else:
                        print("❌ 格式: message-file <会话ID> <文件路径>")
                elif command:
                    print("❌ 未知命令，输入 'help' 查看帮助")
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")

if __name__ == "__main__":
    import sys
    main() 