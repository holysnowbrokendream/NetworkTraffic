from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='部门')
    role = models.CharField(max_length=50, default='user', verbose_name='角色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return f"{self.user.username} - {self.role}" 