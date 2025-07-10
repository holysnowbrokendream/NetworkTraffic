from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """获取仪表板总览数据"""
    overview_data = {
        'today_traffic': '2.5 GB',
        'abnormal_traffic': 15,
        'model_alerts': 8,
        'system_status': '正常',
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return Response(overview_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def traffic_trends(request):
    """获取流量趋势数据"""
    # 模拟一周的流量趋势数据
    trends_data = {
        'x': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        'y': [120, 200, 150, 80, 70, 110, 130]
    }
    
    return Response(trends_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alerts_list(request):
    """获取告警列表"""
    alerts = [
        {
            'id': 1,
            'type': '异常流量',
            'message': '检测到来自192.168.1.100的异常流量',
            'level': 'high',
            'time': '2024-01-15 14:30:00',
            'status': 'unread'
        },
        {
            'id': 2,
            'type': '模型告警',
            'message': '模型检测到潜在的DDoS攻击',
            'level': 'medium',
            'time': '2024-01-15 13:45:00',
            'status': 'read'
        },
        {
            'id': 3,
            'type': '系统告警',
            'message': '磁盘使用率超过80%',
            'level': 'low',
            'time': '2024-01-15 12:20:00',
            'status': 'read'
        }
    ]
    
    return Response(alerts) 