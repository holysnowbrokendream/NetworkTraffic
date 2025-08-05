#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试CLI工具的登录和token保存功能
"""

import requests
import json

def test_login():
    """测试登录功能"""
    base_url = "http://localhost:8000"
    headers = {'Content-Type': 'application/json'}
    
    # 测试登录
    data = {'username': 'hxh', 'password': '123456'}
    response = requests.post(f"{base_url}/login/", json=data, headers=headers)
    
    print(f"登录响应状态码: {response.status_code}")
    print(f"登录响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            token = result.get('token') or result.get('access')
            print(f"获取到token: {token[:20]}...")
            
            # 测试使用token访问API
            headers['Authorization'] = f'Bearer {token}'
            sessions_response = requests.get(f"{base_url}/api/modeltask/sessions/", headers=headers)
            
            print(f"会话API响应状态码: {sessions_response.status_code}")
            print(f"会话API响应内容: {sessions_response.text}")
            
            return True
        else:
            print("登录失败")
            return False
    else:
        print("登录请求失败")
        return False

if __name__ == "__main__":
    test_login() 