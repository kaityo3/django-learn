from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.index,name="index"),
    path("user_list/", views.user_list,name="user_list"),
    path("register/", views.register,name="register"),
    path("user_login/", views.user_login,name="user_login"),
    path("user_logout/", views.user_logout,name="user_logout"),
    path("info/", views.info,name="info"),
]
