from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def model_analysis(request):
    """获取模型分析结果"""
    # 模拟模型分析结果
    analysis_result = {
        'total_records': 10000,
        'abnormal_count': 150,
        'accuracy': 0.95,
        'precision': 0.92,
        'recall': 0.88,
        'f1_score': 0.90,
        'model_version': 'v1.2.0',
        'last_updated': '2024-01-15 10:30:00'
    }
    
    return Response(analysis_result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def train_model(request):
    """训练模型"""
    # 模拟模型训练
    training_result = {
        'status': 'training',
        'progress': 0,
        'estimated_time': '2小时',
        'message': '模型训练已开始'
    }
    
    return Response(training_result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def model_status(request):
    """获取模型状态"""
    status_info = {
        'status': 'ready',
        'version': 'v1.2.0',
        'last_trained': '2024-01-15 08:00:00',
        'performance': {
            'accuracy': 0.95,
            'precision': 0.92,
            'recall': 0.88
        }
    }
    
    return Response(status_info)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def abnormal_distribution(request):
    """获取异常分布数据"""
    distribution_data = [
        {'value': 1048, 'name': '端口扫描'},
        {'value': 735, 'name': 'DDoS'},
        {'value': 580, 'name': '恶意登录'},
        {'value': 484, 'name': '数据泄露'},
        {'value': 300, 'name': 'SQL注入'},
        {'value': 250, 'name': 'XSS攻击'},
    ]
    
    return Response(distribution_data) 