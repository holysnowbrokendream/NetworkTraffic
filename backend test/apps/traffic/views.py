import os
import pandas as pd
from datetime import datetime, timedelta
from django.db.models import Q, Sum, Count
from django.utils import timezone
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import TrafficFile, TrafficRecord, TrafficStatistics
from .serializers import (
    TrafficFileSerializer, TrafficRecordSerializer, 
    TrafficStatisticsSerializer, FileUploadSerializer
)


class TrafficFileListView(generics.ListCreateAPIView):
    """流量文件列表"""
    permission_classes = [IsAuthenticated]
    serializer_class = TrafficFileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['file_name']
    ordering_fields = ['upload_time', 'file_size']
    ordering = ['-upload_time']

    def get_queryset(self):
        return TrafficFile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TrafficFileDetailView(generics.RetrieveDestroyAPIView):
    """流量文件详情"""
    permission_classes = [IsAuthenticated]
    serializer_class = TrafficFileSerializer

    def get_queryset(self):
        return TrafficFile.objects.filter(user=self.request.user)


class TrafficRecordListView(generics.ListAPIView):
    """流量记录列表"""
    permission_classes = [IsAuthenticated]
    serializer_class = TrafficRecordSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['src_ip', 'dst_ip', 'protocol']
    ordering_fields = ['timestamp', 'packet_size']
    ordering = ['-timestamp']

    def get_queryset(self):
        queryset = TrafficRecord.objects.all()
        
        # 过滤条件
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        src_ip = self.request.query_params.get('src_ip', None)
        if src_ip:
            queryset = queryset.filter(src_ip__icontains=src_ip)
        
        dst_ip = self.request.query_params.get('dst_ip', None)
        if dst_ip:
            queryset = queryset.filter(dst_ip__icontains=dst_ip)
        
        # 时间范围过滤
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
        
        return queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """上传流量文件"""
    parser_classes = (MultiPartParser, FormParser)
    
    serializer = FileUploadSerializer(data=request.data)
    if serializer.is_valid():
        uploaded_file = serializer.validated_data['file']
        
        # 创建文件记录
        file_extension = uploaded_file.name.split('.')[-1].lower()
        traffic_file = TrafficFile.objects.create(
            user=request.user,
            file=uploaded_file,
            file_type=file_extension,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            status='uploading'
        )
        
        # 异步处理文件（这里简化处理）
        try:
            # 模拟文件处理
            traffic_file.status = 'processing'
            traffic_file.save()
            
            # 这里应该启动异步任务处理文件
            # process_traffic_file.delay(traffic_file.id)
            
            return Response({
                'message': '文件上传成功，正在处理中',
                'file_id': traffic_file.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            traffic_file.status = 'failed'
            traffic_file.error_message = str(e)
            traffic_file.save()
            return Response({
                'error': f'文件处理失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def traffic_statistics(request):
    """获取流量统计"""
    # 获取查询参数
    days = int(request.query_params.get('days', 7))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # 查询统计数据
    stats = TrafficStatistics.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # 如果没有统计数据，生成模拟数据
    if not stats.exists():
        stats_data = []
        for i in range(days):
            date = end_date - timedelta(days=i)
            stats_data.append({
                'date': date,
                'total_packets': 1000 + (i * 100),
                'total_bytes': 1024 * 1024 * (10 + i),
                'normal_packets': 950 + (i * 90),
                'abnormal_packets': 30 + (i * 5),
                'suspicious_packets': 20 + (i * 5),
            })
    else:
        stats_data = TrafficStatisticsSerializer(stats, many=True).data
    
    return Response({
        'period': f'{start_date} 到 {end_date}',
        'data': stats_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def traffic_overview(request):
    """获取流量总览"""
    today = timezone.now().date()
    
    # 今日统计
    today_stats = TrafficStatistics.objects.filter(date=today).first()
    if not today_stats:
        today_stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'abnormal_packets': 0,
        }
    else:
        today_stats = TrafficStatisticsSerializer(today_stats).data
    
    # 异常流量统计
    abnormal_count = TrafficRecord.objects.filter(
        status__in=['abnormal', 'suspicious'],
        timestamp__date=today
    ).count()
    
    # 最近7天趋势
    week_stats = []
    for i in range(7):
        date = today - timedelta(days=i)
        day_stats = TrafficStatistics.objects.filter(date=date).first()
        if day_stats:
            week_stats.append({
                'date': date.strftime('%m-%d'),
                'packets': day_stats.total_packets,
                'abnormal': day_stats.abnormal_packets + day_stats.suspicious_packets
            })
        else:
            week_stats.append({
                'date': date.strftime('%m-%d'),
                'packets': 0,
                'abnormal': 0
            })
    
    return Response({
        'today': {
            'total_packets': today_stats.get('total_packets', 0),
            'total_bytes': today_stats.get('total_bytes', 0),
            'abnormal_count': abnormal_count,
        },
        'week_trend': list(reversed(week_stats))
    }) 