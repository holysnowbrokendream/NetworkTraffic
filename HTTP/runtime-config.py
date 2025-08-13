#!/usr/bin/env python3
"""
Runtime Configuration Script
用于在Docker容器运行时动态配置网络访问
"""

import os
import socket
import json
from pathlib import Path

def get_host_ip():
    """获取宿主机IP地址"""
    try:
        # 尝试从环境变量获取
        host_ip = os.getenv('HOST_IP')
        if host_ip:
            return host_ip
        
        # 自动检测IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host_ip = s.getsockname()[0]
        s.close()
        return host_ip
    except:
        return "127.0.0.1"

def create_runtime_config():
    """创建运行时配置文件"""
    host_ip = get_host_ip()
    
    config = {
        "ALLOWED_HOSTS": f"localhost,127.0.0.1,{host_ip},0.0.0.0,*",
        "CSRF_TRUSTED_ORIGINS": f"http://localhost:23456,http://{host_ip}:23456,http://127.0.0.1:23456,http://0.0.0.0:23456",
        "HOST_IP": host_ip
    }
    
    # 写入配置文件
    config_file = Path("/app/config/runtime.json")
    config_file.parent.mkdir(exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Runtime configuration created for host IP: {host_ip}")
    return config

if __name__ == "__main__":
    create_runtime_config()
