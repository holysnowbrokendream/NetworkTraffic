from django.urls import path
from .views import ModelAnalyzeView, ChatSessionListView, ChatSessionDetailView, ChatMessageCreateView

urlpatterns = [
    path('analyze/', ModelAnalyzeView.as_view(), name='model-analyze'),
    path('sessions/', ChatSessionListView.as_view(), name='chat-session-list'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='chat-session-detail'),
    path('sessions/<int:session_id>/messages/', ChatMessageCreateView.as_view(), name='chat-message-create'),
] 