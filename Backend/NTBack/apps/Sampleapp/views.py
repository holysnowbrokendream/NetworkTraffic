from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import UserAccount
import json
from django.utils import timezone

# Create your views here.
def HomePage(request):
    index = [
        "Hello World, You're at the index page!",
        "This is a sample app for Django.",
        "and it's a test version :)"
    ]
    
    # 添加更多上下文数据
    context = {
        'index': index,
        'page_title': '首页',
        'current_time': '2024年',
        'system_status': '运行正常'
    }
    
    return render(request, 'home.html', context)

def Signup(request):
    if request.method == 'GET':
        return render(request, 'Signup.html')
    
    elif request.method == 'POST':
        try:
            # 获取表单数据
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            phonenumber = request.POST.get('phonenumber', '').strip()
            password = request.POST.get('password', '')
            user_type = request.POST.get('user_type', 'user')
            
            # 基本验证
            if not username:
                return JsonResponse({'status': 'error', 'message': '用户名不能为空'})
            
            if not phonenumber:
                return JsonResponse({'status': 'error', 'message': '手机号不能为空'})
            
            if not password:
                return JsonResponse({'status': 'error', 'message': '密码不能为空'})
            
            # 创建用户
            user = UserAccount.objects.create(
                username=username,
                email=email if email else None,
                phonenumber=phonenumber,
                password=password,  # 注意：实际应用中应该加密密码
                user_type=user_type
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': f'用户 {username} 注册成功！'
            })
            
        except IntegrityError as e:
            error_msg = str(e)
            if 'username' in error_msg:
                return JsonResponse({'status': 'error', 'message': '用户名已存在'})
            elif 'email' in error_msg and email:
                return JsonResponse({'status': 'error', 'message': '邮箱已存在'})
            elif 'phonenumber' in error_msg:
                return JsonResponse({'status': 'error', 'message': '手机号已存在'})
            else:
                return JsonResponse({'status': 'error', 'message': '数据重复，请检查输入信息'})
                
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': '注册失败，请稍后重试'})

def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html')
    
    elif request.method == 'POST':
        try:
            login_method = request.POST.get('login_method', 'username')
            password = request.POST.get('password', '')
            remember_me = request.POST.get('remember_me') == 'on'
            
            # 根据登录方式获取用户标识
            if login_method == 'username':
                identifier = request.POST.get('username', '').strip()
                if not identifier:
                    return JsonResponse({'status': 'error', 'message': '用户名不能为空'})
                
                # 查找用户
                try:
                    user = UserAccount.objects.get(username=identifier)
                except UserAccount.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': '用户名不存在'})
                    
            elif login_method == 'phone':
                identifier = request.POST.get('phone', '').strip()
                if not identifier:
                    return JsonResponse({'status': 'error', 'message': '手机号不能为空'})
                
                # 验证手机号格式
                if not identifier.isdigit() or len(identifier) != 11:
                    return JsonResponse({'status': 'error', 'message': '请输入有效的11位手机号'})
                
                # 查找用户
                try:
                    user = UserAccount.objects.get(phonenumber=identifier)
                except UserAccount.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': '手机号未注册'})
                    
            elif login_method == 'email':
                identifier = request.POST.get('email', '').strip()
                if not identifier:
                    return JsonResponse({'status': 'error', 'message': '邮箱不能为空'})
                
                # 查找用户
                try:
                    user = UserAccount.objects.get(email=identifier)
                except UserAccount.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': '邮箱未注册'})
            else:
                return JsonResponse({'status': 'error', 'message': '无效的登录方式'})
            
            # 验证密码
            if not password:
                return JsonResponse({'status': 'error', 'message': '密码不能为空'})
            
            # 注意：这里应该使用加密后的密码比较
            # 实际应用中建议使用Django的认证系统
            if user.password == password:  # 简单比较，实际应该加密
                # 登录成功
                # 这里可以设置session或使用Django的login函数
                # 如果使用Django认证系统，需要先创建User对象
                
                # 设置session
                request.session['user_id'] = str(user.id)
                request.session['username'] = user.username
                request.session['user_type'] = user.user_type
                
                # 如果选择记住我，设置更长的session过期时间
                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30天
                else:
                    request.session.set_expiry(0)  # 浏览器关闭时过期
                
                return JsonResponse({
                    'status': 'success', 
                    'message': f'欢迎回来，{user.username}！'
                })
            else:
                return JsonResponse({'status': 'error', 'message': '密码错误'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': '登录失败，请稍后重试'})

# 检查用户是否已登录的装饰器
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper

# 需要登录才能访问的页面示例
@login_required_custom
@csrf_exempt
def Dashboard(request):
    user_id = request.session.get('user_id')
    user = UserAccount.objects.get(id=user_id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            phonenumber = data.get('phonenumber', '').strip()
            password = data.get('password', '').strip()
            # 邮箱和手机号唯一性校验
            if email and email != user.email and UserAccount.objects.filter(email=email).exclude(id=user_id).exists():
                return JsonResponse({'status': 'error', 'message': '邮箱已被占用'})
            if phonenumber and phonenumber != user.phonenumber and UserAccount.objects.filter(phonenumber=phonenumber).exclude(id=user_id).exists():
                return JsonResponse({'status': 'error', 'message': '手机号已被占用'})
            if email: user.email = email
            if phonenumber: user.phonenumber = phonenumber
            if password: user.password = password  # 实际项目应加密
            user.save()
            return JsonResponse({'status': 'success', 'message': '信息修改成功'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': '修改失败，请重试'})
    context = {
        'username': user.username,
        'user_type': user.user_type,
        'email': user.email,
        'phonenumber': user.phonenumber,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M'),
    }
    return render(request, 'Dashboard.html', context)

# 登出功能 - 直接返回home页面
def Logout(request):
    # 清除session
    request.session.flush()
    # 直接重定向到首页
    return redirect('home')
