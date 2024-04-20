from django.urls import path
from . import views

app_name = "form_app"

urlpatterns = [
    path("", views.index,name="index"),
    path("form_student/", views.form_student,name="form_student"),
    path("form_student_update/", views.form_student_update,name="form_student_update"),
    path("students_list/", views.students_list,name="students_list"),
    path("teached_update_student/<int:id>", views.update_student,name="update_student"),
    path("delete_student/<int:id>", views.delete_student,name="delete_student"),
]
