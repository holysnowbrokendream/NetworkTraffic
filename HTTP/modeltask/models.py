from django.db import models
from userauth.models import Users
import os

# 直接用Django自带的JSONField
# from django.contrib.postgres.fields import JSONField  # 删除这一行

# Create your models here.

class UserFile(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='files', verbose_name='所属用户')
    filename = models.CharField(max_length=255, verbose_name='文件名')
    file = models.FileField(upload_to='user_files/', verbose_name='文件')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"{self.filename} ({self.user_id})"

    class Meta:
        db_table = 'user_files'
        verbose_name = '用户文件'
        verbose_name_plural = '用户文件'

# 历史会话模型
class UserSession(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sessions', verbose_name='所属用户')
    name = models.CharField(max_length=255, verbose_name='会话名称', default='新会话')
    messages = models.JSONField(verbose_name='会话消息内容')  # [{role, content, ...}, ...]，文件消息需有type: 'file'等标记
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"{self.name} ({self.user_id})"

    class Meta:
        db_table = 'user_sessions'
        verbose_name = '用户历史会话'
        verbose_name_plural = '用户历史会话'
