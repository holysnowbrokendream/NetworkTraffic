from django.urls import path
from . import views

urlpatterns = [
    # 流量分析报告模式
    path('traffic_analysis_report/', views.traffic_analysis_report, name='traffic_analysis_report'),
    
    # 自定义流量生成模式
    path('custom_traffic_generation/', views.custom_traffic_generation, name='custom_traffic_generation'),
    
    # 流量规则提取模式
    path('traffic_rules_extraction/', views.traffic_rules_extraction, name='traffic_rules_extraction'),
] 