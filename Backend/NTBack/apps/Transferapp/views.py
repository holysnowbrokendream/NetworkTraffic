from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views import View
from .models import UserAccount
import json
import uuid
from django.utils import timezone
import hashlib

# Create your views here.
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

# 工具函数：简单的密码加密
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 工具函数：验证密码
def verify_password(password, hashed_password):
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password

# 工具函数：生成简单的JWT令牌（实际项目应使用专业的JWT库）
def generate_token(user_id):
    import time
    import base64
    token_data = {
        'user_id': str(user_id),
        'timestamp': time.time()
    }
    token_string = json.dumps(token_data)
    return base64.b64encode(token_string.encode()).decode()

# 工具函数：验证令牌
def verify_token(token):
    try:
        import base64
        token_string = base64.b64decode(token.encode()).decode()
        token_data = json.loads(token_string)
        return token_data.get('user_id')
    except:
        return None

# API: 用户注册
@csrf_exempt
@require_http_methods(["POST"])
def register_api(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        phonenumber = data.get('phonenumber', '').strip()
        password = data.get('password', '')
        user_type = data.get('user_type', 'user')
        
        # 基本验证
        if not username:
            return JsonResponse({'status': 'error', 'message': '用户名不能为空'}, status=400)
        
        if not phonenumber:
            return JsonResponse({'status': 'error', 'message': '手机号不能为空'}, status=400)
        
        if not password:
            return JsonResponse({'status': 'error', 'message': '密码不能为空'}, status=400)
        
        # 检查用户是否已存在
        if UserAccount.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': '用户名已存在'}, status=400)
        
        if UserAccount.objects.filter(phonenumber=phonenumber).exists():
            return JsonResponse({'status': 'error', 'message': '手机号已存在'}, status=400)
        
        if email and UserAccount.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': '邮箱已存在'}, status=400)
        
        # 创建用户
        user = UserAccount.objects.create(
            username=username,
            email=email if email else None,
            phonenumber=phonenumber,
            password=hash_password(password),
            user_type=user_type
        )
        
        return JsonResponse({
            'status': 'success',
            'message': f'用户 {username} 注册成功！',
            'user_id': str(user.id)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': '注册失败，请稍后重试'}, status=500)

# API: 用户登录
@csrf_exempt
@require_http_methods(["POST"])
def login_api(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username:
            return JsonResponse({'status': 'error', 'message': '用户名不能为空'}, status=400)
        
        if not password:
            return JsonResponse({'status': 'error', 'message': '密码不能为空'}, status=400)
        
        # 查找用户（支持用户名、邮箱、手机号登录）
        user = None
        try:
            # 先尝试用户名
            user = UserAccount.objects.get(username=username)
        except UserAccount.DoesNotExist:
            try:
                # 再尝试邮箱
                user = UserAccount.objects.get(email=username)
            except UserAccount.DoesNotExist:
                try:
                    # 最后尝试手机号
                    user = UserAccount.objects.get(phonenumber=username)
                except UserAccount.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': '用户不存在'}, status=404)
        
        # 验证密码
        if not verify_password(password, user.password):
            return JsonResponse({'status': 'error', 'message': '密码错误'}, status=401)
        
        # 生成令牌
        token = generate_token(user.id)
        
        return JsonResponse({
            'status': 'success',
            'message': f'欢迎回来，{user.username}！',
            'token': token,
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phonenumber': user.phonenumber,
                'user_type': user.user_type,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat()
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': '登录失败，请稍后重试'}, status=500)

# API: 获取用户信息
@csrf_exempt
@require_http_methods(["GET"])
def user_info_api(request):
    try:
        # 从请求头获取令牌
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'status': 'error', 'message': '未提供有效的令牌'}, status=401)
        
        token = auth_header[7:]  # 移除 'Bearer ' 前缀
        user_id = verify_token(token)
        
        if not user_id:
            return JsonResponse({'status': 'error', 'message': '令牌无效'}, status=401)
        
        # 查找用户
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '用户不存在'}, status=404)
        
        return JsonResponse({
            'status': 'success',
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phonenumber': user.phonenumber,
                'user_type': user.user_type,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': '获取用户信息失败'}, status=500)

# API: 更新用户信息
@csrf_exempt
@require_http_methods(["PUT"])
def update_user_api(request):
    try:
        # 从请求头获取令牌
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'status': 'error', 'message': '未提供有效的令牌'}, status=401)
        
        token = auth_header[7:]  # 移除 'Bearer ' 前缀
        user_id = verify_token(token)
        
        if not user_id:
            return JsonResponse({'status': 'error', 'message': '令牌无效'}, status=401)
        
        # 查找用户
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '用户不存在'}, status=404)
        
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        phonenumber = data.get('phonenumber', '').strip()
        password = data.get('password', '').strip()
        
        # 邮箱唯一性校验
        if email and email != user.email:
            if UserAccount.objects.filter(email=email).exclude(id=user_id).exists():
                return JsonResponse({'status': 'error', 'message': '邮箱已被占用'}, status=400)
            user.email = email
        
        # 手机号唯一性校验
        if phonenumber and phonenumber != user.phonenumber:
            if UserAccount.objects.filter(phonenumber=phonenumber).exclude(id=user_id).exists():
                return JsonResponse({'status': 'error', 'message': '手机号已被占用'}, status=400)
            user.phonenumber = phonenumber
        
        # 密码更新
        if password:
            user.password = hash_password(password)
        
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': '信息修改成功',
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phonenumber': user.phonenumber,
                'user_type': user.user_type,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat()
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': '修改失败，请重试'}, status=500)

# API: 系统首页信息
@csrf_exempt
@require_http_methods(["GET"])
def home_api(request):
    try:
        index_info = [
            "Hello World, You're at the API version!",
            "This is a RESTful API for Network Traffic Analysis.",
            "Frontend and backend are now separated :)"
        ]
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'index': index_info,
                'page_title': '网络流量分析系统API',
                'current_time': timezone.now().isoformat(),
                'system_status': '运行正常'
            }
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': '获取首页信息失败'}, status=500)
