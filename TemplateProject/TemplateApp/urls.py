from django.urls import path
from . import views

app_name = "template_app"

urlpatterns=[
    # hello部分を空白("")にするとfirst_app直下がリンク先になる
    path("", views.index,name="index"),
    path("home/<first_name>/<last_name>", views.home,name="home"),
    path("sample1", views.sample1,name="sample1"),
    path("sample2", views.sample2,name="sample2"),
    path("sample3", views.sample3,name="sample3"),
    path("sample", views.sample,name="sample"),
]
