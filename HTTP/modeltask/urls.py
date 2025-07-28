from django.urls import path
from .views import CreateTxtFileView, MultiUploadView, ListUserFilesView, DeleteUserFileView
from . import views

urlpatterns = [
    path('create_txt_file/', CreateTxtFileView.as_view()),
    path('multi_upload/', MultiUploadView.as_view()),
    path('list_user_files/', ListUserFilesView.as_view()),
    path('delete_user_file/', DeleteUserFileView.as_view()),
    path('save_session/', views.save_session, name='save_session'),
    path('list_sessions/', views.list_sessions, name='list_sessions'),
    path('get_session/<int:session_id>/', views.get_session, name='get_session'),
    path('delete_session/', views.delete_session, name='delete_session'),
    path('rename_session/', views.rename_session, name='rename_session'),
] 