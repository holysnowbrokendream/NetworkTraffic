from django.urls import path
from .views import (
    TrafficFileListView, TrafficFileDetailView, TrafficRecordListView,
    upload_file, traffic_statistics, traffic_overview
)

urlpatterns = [
    path('files/', TrafficFileListView.as_view(), name='file-list'),
    path('files/<int:pk>/', TrafficFileDetailView.as_view(), name='file-detail'),
    path('records/', TrafficRecordListView.as_view(), name='record-list'),
    path('upload/', upload_file, name='upload-file'),
    path('statistics/', traffic_statistics, name='traffic-statistics'),
    path('overview/', traffic_overview, name='traffic-overview'),
] 