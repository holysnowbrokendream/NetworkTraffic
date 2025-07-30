from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import requests

# Create your views here.

@csrf_exempt
def traffic_analysis_report(request):
    """
    流量分析报告模式
    用户上传pcap文件，返回report.txt文件
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pcap_file = data.get('pcap_file')
            
            # 验证文件类型
            if pcap_file and not pcap_file.lower().endswith(('.pcap', '.pcapng')):
                return JsonResponse({
                    'status': 'error',
                    'message': '流量分析报告模式需要上传pcap格式的文件（.pcap或.pcapng）'
                }, status=400)
            
            # 从settings获取工具A接口配置
            tool_config = settings.TOOL_INTERFACES['TRAFFIC_ANALYSIS']
            tool_url = tool_config['URL']
            
            response = requests.post(tool_url, json={
                'pcap_file': pcap_file
            }, timeout=settings.TOOL_TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                return JsonResponse({
                    'status': 'success',
                    'filename': 'report.txt',
                    'content': result.get('report_content', ''),
                    'message': '流量分析报告生成成功'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'{tool_config["NAME"]}接口调用失败，状态码: {response.status_code}'
                }, status=500)
                
        except requests.exceptions.Timeout:
            return JsonResponse({
                'status': 'error',
                'message': f'{tool_config["NAME"]}接口调用超时'
            }, status=408)
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'status': 'error',
                'message': f'无法连接到{tool_config["NAME"]}，请检查服务是否启动'
            }, status=503)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'流量分析报告生成失败: {str(e)}'
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)

@csrf_exempt
def custom_traffic_generation(request):
    """
    自定义流量生成模式
    用户输入流量生成规则，返回pcap.txt文件
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            traffic_rules = data.get('traffic_rules')
            
            # 从settings获取工具B接口配置
            tool_config = settings.TOOL_INTERFACES['CUSTOM_TRAFFIC']
            tool_url = tool_config['URL']
            
            response = requests.post(tool_url, json={
                'traffic_rules': traffic_rules
            }, timeout=settings.TOOL_TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                return JsonResponse({
                    'status': 'success',
                    'filename': 'pcap.txt',
                    'content': result.get('pcap_content', ''),
                    'message': '自定义流量生成成功'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'{tool_config["NAME"]}接口调用失败，状态码: {response.status_code}'
                }, status=500)
        
        # 超时408、连接错误503、异常处理400
        except requests.exceptions.Timeout:
            return JsonResponse({
                'status': 'error',
                'message': f'{tool_config["NAME"]}接口调用超时'
            }, status=408)
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'status': 'error',
                'message': f'无法连接到{tool_config["NAME"]}，请检查服务是否启动'
            }, status=503)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'自定义流量生成失败: {str(e)}'
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)

@csrf_exempt
def traffic_rules_extraction(request):
    """
    流量规则提取模式
    用户上传pcap文件，返回rules.txt文件
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pcap_file = data.get('pcap_file')
            
            # 验证文件类型
            if pcap_file and not pcap_file.lower().endswith(('.pcap', '.pcapng')):
                return JsonResponse({
                    'status': 'error',
                    'message': '流量规则提取模式需要上传pcap格式的文件（.pcap或.pcapng）'
                }, status=400)
            
            # 从settings获取工具C接口配置
            tool_config = settings.TOOL_INTERFACES['TRAFFIC_RULES']
            tool_url = tool_config['URL']
            
            response = requests.post(tool_url, json={
                'pcap_file': pcap_file
            }, timeout=settings.TOOL_TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                return JsonResponse({
                    'status': 'success',
                    'filename': 'rules.txt',
                    'content': result.get('rules_content', ''),
                    'message': '流量规则提取成功'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'{tool_config["NAME"]}接口调用失败，状态码: {response.status_code}'
                }, status=500)
                
        except requests.exceptions.Timeout:
            return JsonResponse({
                'status': 'error',
                'message': f'{tool_config["NAME"]}接口调用超时'
            }, status=408)
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'status': 'error',
                'message': f'无法连接到{tool_config["NAME"]}，请检查服务是否启动'
            }, status=503)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'流量规则提取失败: {str(e)}'
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)
