from django.urls import path
from . import views

app_name = "rikujobu_app"

urlpatterns=[
    # hello部分を空白("")にするとfirst_app直下がリンク先になる
    path("home", views.home,name="home"),
    path("members", views.members,name="members"),
    path("person/<int:id>", views.person,name="person")
]
