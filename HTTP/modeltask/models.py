from django.db import models
from userauth.models import Users
import os

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
