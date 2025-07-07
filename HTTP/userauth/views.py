from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userauth.models import Users
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json

# Create your views here.

@csrf_exempt
# 用户注册接口，支持POST请求，参数为username和password
# 返回注册结果的JSON响应

def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 解析请求体中的JSON数据
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                # 缺少参数
                return JsonResponse({'status': 'fail', 'msg': '缺少参数'}, status=400)
            if User.objects.filter(username=username).exists():
                # 用户名已存在
                return JsonResponse({'status': 'fail', 'msg': '用户名已存在'}, status=409)
            # 创建新用户
            User.objects.create_user(username=username, password=password)
            return JsonResponse({'status': 'success', 'msg': '注册成功'})
        except Exception as e:
            # 其他异常
            return JsonResponse({'status': 'fail', 'msg': str(e)}, status=400)
    else:
        # 只允许POST请求
        return JsonResponse({'status': 'fail', 'msg': '只支持POST请求'}, status=405)

@csrf_exempt
# 用户登录接口，支持POST请求，参数为username和password
# 返回登录结果的JSON响应

def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 解析请求体中的JSON数据
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                # 缺少参数
                return JsonResponse({'status': 'fail', 'msg': '缺少参数'}, status=400)
            user = authenticate(username=username, password=password)
            if user is not None:
                # 登录成功
                return JsonResponse({'status': 'success', 'msg': '登录成功'})
            else:
                # 用户名或密码错误
                return JsonResponse({'status': 'fail', 'msg': '用户名或密码错误'}, status=401)
        except Exception as e:
            # 其他异常
            return JsonResponse({'status': 'fail', 'msg': str(e)}, status=400)
    else:
        # 只允许POST请求
        return JsonResponse({'status': 'fail', 'msg': '只支持POST请求'}, status=405)

@csrf_exempt
def llm_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            messages = data.get('messages', [])
            file_ids = data.get('file_ids', [])
            user_msg = messages[-1]['content'] if messages else ''
            if file_ids:
                reply = f'模拟回复：你说的是"{user_msg}"，你已上传文件：{",".join(file_ids)}'
            else:
                reply = f'模拟回复：你说的是"{user_msg}"'
            return JsonResponse({'reply': reply})
        except Exception as e:
            return JsonResponse({'reply': f'发生错误: {str(e)}'}, status=400)
    return JsonResponse({'error': '仅支持POST'}, status=405)

@csrf_exempt
def llm_upload(request):
    if request.method == 'POST':
        return JsonResponse({'file_id': request.FILES['file'].name, 'msg': '上传成功'})
    return JsonResponse({'error': '仅支持POST'}, status=405)
