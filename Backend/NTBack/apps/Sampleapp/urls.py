from django.urls import path, include
from . import views

urlpatterns = [
    path("home/", views.HomePage, name="home"),
    path("signup/", views.Signup, name="signup"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("dashboard/", views.Dashboard, name="dashboard"),
]