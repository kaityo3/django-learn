from django.shortcuts import render
from . import forms
from django.forms import modelformset_factory
from .models import Students
from django.core.files.storage import FileSystemStorage
import os

def index(request):
    return render(request, "formapp/index.html")

# def form_student(request):
#     user = None
#     if request.method == "POST":
#         form = forms.StudentForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#     else:
#         form = forms.StudentForm()
#     return render(
#         request,
#         "formapp/upload_student.html",
#         context={
#             "form": form,
#             "user": user,
#         }
#     )

def form_student(request):
    user = None
    form = forms.StudentForm(data = request.POST or None, files=request.FILES or None)
    if form.is_valid():
        print("Aa")
        user = form.save()
        # save時にformの中身を初期化して、画面上に値が残り続けるのを防止する。
        form = forms.StudentForm()

    return render(
        request,
        "formapp/upload_student.html",
        context={
            "form": form,
            "user": user,
        }
    )

def form_student_update(request):
    formset = modelformset_factory(Students,forms.StudentForm, extra=2)
    if request.method == "POST":
        formset = formset(request.POST, request.FILES)
        if formset.is_valid:
            formset.save()

    return render(
        request,
        "formapp/update_student.html",
        context={
            "formset": formset,
        }
    )

def students_list(request):
    students = Students.objects.all()
    return render(
        request,
        "formapp/students_list.html",
        context={
            "students": students
        }
    )

def update_student(request, id):
    student = Students.objects.get(pk=id)
    
    if request.method == "POST":
        update_form=forms.StudentUpdateForm(data = request.POST or None, files=request.FILES or None)
        if update_form.is_valid():
            student.name = update_form.cleaned_data["name"]
            student.age = update_form.cleaned_data["age"]
            student.grade = update_form.cleaned_data["grade"]

            # student.picture = update_form.cleaned_data["picture"]
            picture = update_form.cleaned_data["picture"]
            if picture:
                # fs = FileSystemStorage()
                # file = fs.save(os.path.join("picture",picture.name), picture)
                student.picture = picture
            student.save()
    # form = の初期状態の定義はPOSTの処理の下に書いたほうが値が即座に更新されていい気がする。    
    form  = forms.StudentUpdateForm(
        initial={
            "name":student.name,
            "age":student.age,
            "grade":student.grade,
            "picture":student.picture,
            }
    )
    
    return render(
        request,
        "formapp/teached_update_student.html",
        context={
            "form":form,
            "student":student
        }
    )

def delete_student(request, id):
    delete_form = forms.StudentDeleteForm(
        initial={
            "id":id
        }
    )
    if request.method =="POST":
        delete_form = forms.StudentDeleteForm(request.POST or None)
        if delete_form.is_valid():
            Students.objects.get(id=delete_form.cleaned_data["id"]).delete()
    return render(
        request,
        "formapp/delete_student.html",
        context={
            "delete_form":delete_form
        }
    )
