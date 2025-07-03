from django.db import models
import uuid

### 创建一个模型类，用于存储数据库中的表结构
class Sample(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# 类中的字段表示数据表中的字段，数据类型由XXXField表示，例如：
# name = models.CharField(max_length=255)
# 表示一个字符串字段，最大长度为255
# age = models.IntegerField()
# 表示一个整数字段
# email = models.EmailField(max_length=255)
# 表示一个电子邮件字段，最大长度为255
# created_at = models.DateTimeField(auto_now_add=True)
# 表示一个日期时间字段，自动设置为当前时间
# updated_at = models.DateTimeField(auto_now=True)
# 表示一个日期时间字段，自动设置为当前时间

### 常见数据类型
# CharField：字符串
# IntegerField：整数
# FloatField：浮点数
# BooleanField：布尔值
# DateField：日期
# TimeField：时间
# DateTimeField：日期时间
# TextField：长文本
# EmailField：电子邮件
# URLField：URL
# FileField：文件
# ImageField：图片
# JSONField：JSON
# ArrayField：数组
# DictField：字典
# UUIDField：UUID
# IPAddressField：IP地址
# GenericIPAddressField：通用IP地址
# SlugField：缩略名
# BinaryField：二进制

### 常见字段参数
# max_length：最大长度
# null：是否允许为空
# blank：是否允许为空
# default：默认值
# choices：选择项
# verbose_name：显示名称
# help_text：帮助文本
# unique：是否唯一
# db_index：是否创建索引
# db_column：数据库列名
# db_table：数据库表名
# db_table_comment：数据库表注释

    ### 模型元数据（可选）
    # 元数据是用于描述模型的元信息，例如：
    # ordering = ['-created_at', 'name']
    # 从前往后按照字段值进行排序，“-”前缀表示倒序，"?"表示随机排序
    # verbose_name = '样例'
    # 表示模型的显示名称
    # verbose_name_plural = '样例'
    # 表示模型的复数名称
    # permissions = []
    # 表示模型的权限
    class Meta:
        ordering = ['-created_at']
        # permissions = []

### Create your models here.
class UserAccount(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    
    # 账号基础信息设置（必填）
    username = models.CharField(
        max_length=255, 
        verbose_name="用户名", 
        unique=True,
        help_text="用户名不能重复"
        )
    email = models.EmailField(
        max_length=255, 
        verbose_name="邮箱", 
        unique=True, 
        blank=True, null=True, 
        help_text="邮箱不能重复"
        )
    phonenumber = models.CharField(
        max_length=16, 
        verbose_name="手机号", 
        unique=True, 
        blank=False, null=False, 
        help_text="手机号不能为空"
        )
    password = models.CharField(
        max_length=255, 
        verbose_name="密码", 
        blank=False, null=False, 
        help_text="密码不能为空"
        )
    
    # 添加用户类型
    USER_TYPE_CHOICES = [
        ('admin', '管理员'),
        ('user', '普通用户'),
        ('guest', '访客'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='user',
        verbose_name="用户类型"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "用户账号"
        verbose_name_plural = "用户账号"
        unique_together = ('username', 'email', 'phonenumber')
    
    def __str__(self):
        return f"{self.username} - {self.email} - {self.phonenumber}"
    
    # 保存账号信息前，验证下列条例
    def save(self, *args, **kwargs):
        if not self.phonenumber:
            raise ValueError("手机号不能为空") 
        if not len(self.phonenumber) <= 16:
            raise ValueError("手机号长度不能超过16位")
        if not self.username:
            self.username = self.phonenumber
        super().save(*args, **kwargs)
