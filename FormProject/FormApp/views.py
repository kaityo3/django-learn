from django.shortcuts import render
from . import forms
from django.forms import formset_factory,modelformset_factory
from .models import ModelSetPost
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.

def index(request):
    return render(request,"formapp/index.html")

def form_page(request):
    form = forms.UserInfo()
    if request.method == "POST":
        form  = forms.UserInfo(request.POST)
        # フィールドの値が正しい場合
        if form.is_valid():
            print("バリデーション成功")
            # print(f"name:{form.cleaned_data['name']},age:{form.cleaned_data['age']},mail:{form.cleaned_data['mail']}")
            print(form.cleaned_data)
    return render(
        request,
        "formapp/form_page.html",
        context={
            "form":form
        }
    )



# def form_post(request):
#     form = forms.PostModelForm()
#     if request.method == "POST":
#         form  = forms.PostModelForm(request.POST)
#         if form.is_valid():
#             print("バリデーション成功")
#             form.save()
#         else:
#             print("バリデーション失敗")

#     return render(
#         request,
#         "formapp/form_post.html",
#         context={
#             "form":form
#         }
#     )

def form_post(request):
    form = forms.PostModelForm(request.POST or None)
    if form.is_valid():
        print("バリデーション成功")
        form.save()
    else:
        print("バリデーション失敗")

    return render(
        request,
        "formapp/form_post.html",
        context={
            "form":form
        }
    )

def form_set_post(request):
    TestFormset = formset_factory(forms.FormSetPost,extra=3)
    formset = TestFormset(request.POST or None)
    if formset.is_valid():
        for form in formset:
            print(form.cleaned_data)

    return render(
        request,
        "formapp/form_set_post.html",
        context={
            "formset": formset
        }
    )


def modelform_set_post(request):
    # TestFormSet = modelformset_factory(ModelSetPost, fields = "__all__", extra=3)
    TestFormSet = modelformset_factory(ModelSetPost, form=forms.ModelFormSetPost, extra=3)
    formset = TestFormSet(request.POST or None)
    if formset.is_valid():
        formset.save()
    return render(
        request,
        "formapp/modelform_set_post.html",
        context={
            "formset": formset
        }
    )

def upload_sample(request):
    if request.method == "POST" and request.FILES["upload_file"]:
        upload_file = request.FILES["upload_file"]
        # ファイルを保存する
        fs = FileSystemStorage() 
        file_path = os.path.join("upload",upload_file.name)
        file = fs.save(file_path, upload_file)
        uploaded_file_url = fs.url(file)

        return render(request, 
                      "formapp/upload_sample.html",
                      context={
                          "uploaded_file_url": uploaded_file_url
                      }
        )
    return render(
        request,
        "formapp/upload_sample.html",
    )

def upload_model_form(request):
    user = None
    if request.method == "POST":
        form = forms.UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
    else:
        form = forms.UserForm()
    return render(request,
                  "formapp/upload_model_form.html",
                  context={
                      "form": form,
                      "user": user
                  }
                  )
