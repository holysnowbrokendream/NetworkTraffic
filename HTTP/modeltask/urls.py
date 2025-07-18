from django.urls import path
from .views import CreateTxtFileView, MultiUploadView, ListUserFilesView, DeleteUserFileView

urlpatterns = [
    path('create_txt_file/', CreateTxtFileView.as_view()),
    path('multi_upload/', MultiUploadView.as_view()),
    path('list_user_files/', ListUserFilesView.as_view()),
    path('delete_user_file/', DeleteUserFileView.as_view()),
] 