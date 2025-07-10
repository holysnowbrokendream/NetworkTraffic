from django.db import models
from django.contrib.auth.models import User


class TrafficFile(models.Model):
    """流量文件模型"""
    FILE_TYPES = [
        ('csv', 'CSV文件'),
        ('pcap', 'PCAP文件'),
        ('psap', 'PSAP文件'),
        ('txt', 'TXT文件'),
    ]
    
    STATUS_CHOICES = [
        ('uploading', '上传中'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='上传用户')
    file = models.FileField(upload_to='traffic_files/', verbose_name='文件')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, verbose_name='文件类型')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_size = models.BigIntegerField(verbose_name='文件大小(字节)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploading', verbose_name='状态')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    process_time = models.DateTimeField(null=True, blank=True, verbose_name='处理完成时间')
    error_message = models.TextField(blank=True, null=True, verbose_name='错误信息')

    class Meta:
        verbose_name = '流量文件'
        verbose_name_plural = '流量文件'
        ordering = ['-upload_time']

    def __str__(self):
        return f"{self.file_name} - {self.get_status_display()}"


class TrafficRecord(models.Model):
    """流量记录模型"""
    STATUS_CHOICES = [
        ('normal', '正常'),
        ('abnormal', '异常'),
        ('suspicious', '可疑'),
    ]
    
    file = models.ForeignKey(TrafficFile, on_delete=models.CASCADE, related_name='records', verbose_name='所属文件')
    timestamp = models.DateTimeField(verbose_name='时间戳')
    src_ip = models.GenericIPAddressField(verbose_name='源IP')
    dst_ip = models.GenericIPAddressField(verbose_name='目的IP')
    src_port = models.IntegerField(null=True, blank=True, verbose_name='源端口')
    dst_port = models.IntegerField(null=True, blank=True, verbose_name='目的端口')
    protocol = models.CharField(max_length=20, verbose_name='协议')
    packet_size = models.BigIntegerField(verbose_name='数据包大小(字节)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '流量记录'
        verbose_name_plural = '流量记录'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['src_ip']),
            models.Index(fields=['dst_ip']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.src_ip} -> {self.dst_ip} ({self.protocol})"


class TrafficStatistics(models.Model):
    """流量统计模型"""
    date = models.DateField(verbose_name='统计日期')
    total_packets = models.BigIntegerField(default=0, verbose_name='总数据包数')
    total_bytes = models.BigIntegerField(default=0, verbose_name='总字节数')
    normal_packets = models.BigIntegerField(default=0, verbose_name='正常数据包数')
    abnormal_packets = models.BigIntegerField(default=0, verbose_name='异常数据包数')
    suspicious_packets = models.BigIntegerField(default=0, verbose_name='可疑数据包数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '流量统计'
        verbose_name_plural = '流量统计'
        unique_together = ['date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - 总包数: {self.total_packets}" 