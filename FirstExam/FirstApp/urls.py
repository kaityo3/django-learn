from django.urls import path
from . import views

app_name = "FirstApp"

urlpatterns=[
    # hello部分を空白("")にするとfirst_app直下がリンク先になる
    path("", views.index,name="index"),
    path("add/<int:num1>/<int:num2>", views.add_page,name="add_page"),
    path("minus/<str:num1>/<str:num2>", views.minus_page,name="minus_page"),
    path("div/<str:num1>/<str:num2>", views.div_page,name="div_page"),
]
