from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.dashboard_overview, name='dashboard-overview'),
    path('trends/', views.traffic_trends, name='traffic-trends'),
    path('alerts/', views.alerts_list, name='alerts-list'),
] 