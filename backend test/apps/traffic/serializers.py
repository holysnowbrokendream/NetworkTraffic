from rest_framework import serializers
from .models import TrafficFile, TrafficRecord, TrafficStatistics


class TrafficFileSerializer(serializers.ModelSerializer):
    """流量文件序列化器"""
    user = serializers.ReadOnlyField(source='user.username')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TrafficFile
        fields = '__all__'
        read_only_fields = ('user', 'file_size', 'status', 'upload_time', 'process_time', 'error_message')


class TrafficRecordSerializer(serializers.ModelSerializer):
    """流量记录序列化器"""
    file_name = serializers.CharField(source='file.file_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TrafficRecord
        fields = '__all__'


class TrafficStatisticsSerializer(serializers.ModelSerializer):
    """流量统计序列化器"""
    class Meta:
        model = TrafficStatistics
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    """文件上传序列化器"""
    file = serializers.FileField()
    
    def validate_file(self, value):
        # 检查文件类型
        allowed_types = ['csv', 'pcap', 'psap', 'txt']
        file_extension = value.name.split('.')[-1].lower()
        
        if file_extension not in allowed_types:
            raise serializers.ValidationError(f'不支持的文件类型: {file_extension}')
        
        # 检查文件大小 (10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('文件大小不能超过10MB')
        
        return value 