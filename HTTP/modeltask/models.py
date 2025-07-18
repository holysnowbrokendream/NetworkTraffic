from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', verbose_name='所属用户')
    filename = models.CharField(max_length=255, verbose_name='文件名')
    file = models.FileField(upload_to='user_files/', verbose_name='文件')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"{self.filename} ({self.user_id})"

    class Meta:
        db_table = 'user_files'
        verbose_name = '用户文件'
        verbose_name_plural = '用户文件'

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=128, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"会话{self.id}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=16, choices=(('user', '用户'), ('ai', 'AI')))
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:20]}..."
