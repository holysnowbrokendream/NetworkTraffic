from django.urls import path
from . import views

urlpatterns = [
    path('analysis/', views.model_analysis, name='model-analysis'),
    path('train/', views.train_model, name='train-model'),
    path('status/', views.model_status, name='model-status'),
    path('abnormal-distribution/', views.abnormal_distribution, name='abnormal-distribution'),
] 