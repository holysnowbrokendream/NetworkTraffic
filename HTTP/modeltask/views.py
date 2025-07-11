from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import FileResponse
from django.conf import settings
from .models import UserFile
from userauth.models import Users
import os, datetime
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

def get_current_custom_user(request):
    """
    根据 request.user 查找自定义 Users 实例。
    假设 Users.id == request.user.username
    """
    try:
        return Users.objects.get(id=request.user.username)
    except Users.DoesNotExist:
        return None

class CreateTxtFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        filename = request.data.get('filename')
        if not filename:
            filetype = request.data.get('filetype', 'pcap')
            filename = 'pcap.txt' if filetype == 'pcap' else 'rules.txt'
        content = request.data.get('content', '')  # 新增：文件内容
        users_obj = get_current_custom_user(request)
        if not users_obj:
            return Response({'msg': '用户不存在'}, status=400)
        rel_path = f'user_files/{users_obj.id}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{filename}'
        abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        userfile = UserFile.objects.create(user=users_obj, filename=filename, file=rel_path)
        # 构造完整的媒体文件URL
        full_url = request.build_absolute_uri(settings.MEDIA_URL + rel_path)
        return Response({'file_id': userfile.id, 'filename': filename, 'url': full_url}, status=201)

class MultiUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        try:
            users_obj = get_current_custom_user(request)
        except Users.DoesNotExist:
            return Response({'msg': '用户不存在'}, status=400)
        files = request.FILES.getlist('file')
        result = []
        for f in files:
            rel_path = f'user_files/{users_obj.id}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{f.name}'
            abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)
            userfile = UserFile.objects.create(user=users_obj, filename=f.name, file=rel_path)
            # 构造完整的媒体文件URL
            full_url = request.build_absolute_uri(settings.MEDIA_URL + rel_path)
            result.append({'file_id': userfile.id, 'filename': f.name, 'url': full_url})
        return Response({'files': result}, status=201)

class ListUserFilesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            users_obj = get_current_custom_user(request)
        except Users.DoesNotExist:
            return Response({'msg': '用户不存在'}, status=400)
        files = UserFile.objects.filter(user=users_obj).order_by('-created_at')
        data = []
        for f in files:
            # 构造完整的媒体文件URL
            full_url = request.build_absolute_uri(settings.MEDIA_URL + str(f.file))
            data.append({'file_id': f.id, 'filename': f.filename, 'url': full_url, 'created_at': f.created_at})
        return Response({'files': data})

class DeleteUserFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        file_id = request.data.get('file_id')
        try:
            users_obj = get_current_custom_user(request)
        except Users.DoesNotExist:
            return Response({'msg': '用户不存在'}, status=400)
        try:
            userfile = UserFile.objects.get(id=file_id, user=users_obj)
            file_path = userfile.file.path
            userfile.delete()
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response({'msg': '删除成功'})
        except UserFile.DoesNotExist:
            return Response({'msg': '文件不存在'}, status=404)

# 定期清理7天前的文件
from django.utils import timezone
from django_cron import CronJobBase, Schedule
class CleanOldFilesCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 * 24  # 每天运行一次
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'modeltask.clean_old_files'
    def do(self):
        week_ago = timezone.now() - datetime.timedelta(days=7)
        old_files = UserFile.objects.filter(created_at__lt=week_ago)
        for f in old_files:
            if os.path.exists(f.file.path):
                os.remove(f.file.path)
            f.delete()
