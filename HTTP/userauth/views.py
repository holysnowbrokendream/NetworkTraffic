from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userauth.models import Users
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json

# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'status': 'fail', 'msg': '缺少参数'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'fail', 'msg': '用户名已存在'}, status=409)
            User.objects.create_user(username=username, password=password)
            return JsonResponse({'status': 'success', 'msg': '注册成功'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'msg': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'fail', 'msg': '只支持POST请求'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'status': 'fail', 'msg': '缺少参数'}, status=400)
            user = authenticate(username=username, password=password)
            if user is not None:
                return JsonResponse({'status': 'success', 'msg': '登录成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '用户名或密码错误'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'msg': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'fail', 'msg': '只支持POST请求'}, status=405)
