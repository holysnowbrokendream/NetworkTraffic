#!/usr/bin/env python3
"""
网络访问配置脚本
用于配置Django应用允许内网访问
"""

import socket
import os
import subprocess
import platform

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 创建一个UDP套接字连接到外部地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def update_settings_file():
    """更新Django设置文件"""
    settings_file = "backend/settings.py"
    
    if not os.path.exists(settings_file):
        print(f"❌ 设置文件不存在: {settings_file}")
        return False
    
    local_ip = get_local_ip()
    print(f"🌐 检测到本机IP地址: {local_ip}")
    
    # 读取当前设置文件
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新ALLOWED_HOSTS
    if f"'{local_ip}'" not in content:
        # 在ALLOWED_HOSTS列表中添加本机IP
        content = content.replace(
            "ALLOWED_HOSTS = [",
            f"ALLOWED_HOSTS = [\n    '{local_ip}',  # 本机IP地址"
        )
        print(f"✅ 已添加本机IP到ALLOWED_HOSTS: {local_ip}")
    
    # 更新CSRF_TRUSTED_ORIGINS
    frontend_url = f"http://{local_ip}:23456"
    if frontend_url not in content:
        # 在CSRF_TRUSTED_ORIGINS列表中添加前端URL
        content = content.replace(
            "CSRF_TRUSTED_ORIGINS = [",
            f"CSRF_TRUSTED_ORIGINS = [\n    '{frontend_url}',  # 前端访问地址"
        )
        print(f"✅ 已添加前端URL到CSRF_TRUSTED_ORIGINS: {frontend_url}")
    
    # 写回文件
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def update_env_file():
    """更新环境变量文件"""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print(f"❌ 环境变量文件不存在: {env_file}")
        return False
    
    local_ip = get_local_ip()
    print(f"🌐 检测到本机IP地址: {local_ip}")
    
    # 读取当前环境变量文件
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新ALLOWED_HOSTS
    if f"{local_ip}" not in content:
        # 在ALLOWED_HOSTS中添加本机IP
        content = content.replace(
            "ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*,your-domain.com,www.your-domain.com",
            f"ALLOWED_HOSTS=localhost,127.0.0.1,{local_ip},0.0.0.0,*,your-domain.com,www.your-domain.com"
        )
        print(f"✅ 已添加本机IP到环境变量ALLOWED_HOSTS: {local_ip}")
    
    # 更新CSRF_TRUSTED_ORIGINS
    frontend_url = f"http://{local_ip}:23456"
    if frontend_url not in content:
        # 在CSRF_TRUSTED_ORIGINS中添加前端URL
        content = content.replace(
            "CSRF_TRUSTED_ORIGINS=http://localhost:3001,http://localhost:23456,http://127.0.0.1:23456,http://0.0.0.0:23456,http://*:23456,https://your-domain.com,https://www.your-domain.com",
            f"CSRF_TRUSTED_ORIGINS=http://localhost:3001,http://localhost:23456,http://127.0.0.1:23456,http://{local_ip}:23456,http://0.0.0.0:23456,http://*:23456,https://your-domain.com,https://www.your-domain.com"
        )
        print(f"✅ 已添加前端URL到环境变量CSRF_TRUSTED_ORIGINS: {frontend_url}")
    
    # 写回文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def show_network_info():
    """显示网络访问信息"""
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🌐 网络访问配置完成!")
    print("="*60)
    print(f"📱 本机IP地址: {local_ip}")
    print(f"🔗 前端访问地址: http://{local_ip}:23456")
    print(f"🔗 后端API地址: http://{local_ip}:8000")
    print(f"🔗 管理界面地址: http://{local_ip}:8000/admin/")
    print("="*60)
    print("💡 同一内网下的其他设备可以通过以上地址访问")
    print("⚠️  请确保防火墙允许8000和23456端口")
    print("="*60)

def check_firewall():
    """检查防火墙设置"""
    system = platform.system().lower()
    
    print("\n🔒 防火墙检查:")
    
    if system == "windows":
        print("Windows系统防火墙检查:")
        try:
            # 检查8000端口
            result = subprocess.run(
                ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"], 
                capture_output=True, text=True
            )
            if "8000" in result.stdout:
                print("✅ 8000端口已配置防火墙规则")
            else:
                print("⚠️  8000端口可能需要配置防火墙规则")
            
            # 检查23456端口
            if "23456" in result.stdout:
                print("✅ 23456端口已配置防火墙规则")
            else:
                print("⚠️  23456端口可能需要配置防火墙规则")
                
        except Exception as e:
            print(f"❌ 无法检查防火墙规则: {e}")
    
    elif system == "linux":
        print("Linux系统防火墙检查:")
        try:
            # 检查iptables规则
            result = subprocess.run(["iptables", "-L"], capture_output=True, text=True)
            if "8000" in result.stdout or "23456" in result.stdout:
                print("✅ 端口已配置防火墙规则")
            else:
                print("⚠️  可能需要配置防火墙规则")
        except Exception as e:
            print(f"❌ 无法检查防火墙规则: {e}")
    
    else:
        print(f"⚠️  未知操作系统: {system}")

def main():
    """主函数"""
    print("🚀 开始配置网络访问...")
    
    # 更新Django设置文件
    if update_settings_file():
        print("✅ Django设置文件更新成功")
    else:
        print("❌ Django设置文件更新失败")
    
    # 更新环境变量文件
    if update_env_file():
        print("✅ 环境变量文件更新成功")
    else:
        print("❌ 环境变量文件更新失败")
    
    # 显示网络信息
    show_network_info()
    
    # 检查防火墙
    check_firewall()
    
    print("\n🎉 网络访问配置完成!")

if __name__ == "__main__":
    main() 