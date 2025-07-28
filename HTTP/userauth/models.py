from django.db import models

# Create your models here.

# 用户表模型，存储用户id和密码
class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=64)  # 用户唯一标识
    pwd = models.CharField(max_length=128)  # 用户密码
    email = models.CharField(max_length=128)  # 用户邮箱

    class Meta:
        db_table = 'users'  # 指定数据库表名
