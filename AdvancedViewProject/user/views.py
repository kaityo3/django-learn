from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.

def user_list(request):
    return render(request,"user/user_list.html")

def index(request):
    return render(request,"user/index.html")

def register(request):
    user_form = forms.UserForm(request.POST or None)
    profile_form = forms.ProfileForm(request.POST or None, request.FILES or None)

    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save(commit=False)
        try:
            # 保存する前のuserを引数に取った方が、確実にvalidateが行われるらしい
            # https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#integrating-validation
            validate_password(user_form.cleaned_data.get("password"),user)
        except ValidationError as e:
            user_form.add_error("password",e)
            return render(
                request,
                "user/registration.html",
                context={
                    "user_form": user_form,
                    "profile_form": profile_form,
                }
            )
        # 暗号化してパスワード保存
        user.set_password(user.password)
        user.save()
        # この場合のcommit=Falseはメモリ上のみで保存するようなものらしい
        profile = profile_form.save(commit=False)
        # profileに1:1で紐づけるuserを代入している
        profile.user = user
        profile.save()

        print("登録完了")
        profile_form = forms.ProfileForm()

    else:
        print("登録失敗")

    return render(
        request,
        "user/registration.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form
        }
    )

def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        if user:
            # "is_active"は関数ではなく単なるbool値を持つ変数なので括弧は不要
            if user.is_active:
                login(request, user)
                return redirect("user:index")
            else:
                return HttpResponse("アカウントがアクティブでないです")
        else:
            return HttpResponse("ユーザーが存在しません")
    return render(
        request,
        "user/login.html",
        context={
            "login_form": login_form
        }
    )

@login_required
def user_logout(request):
    logout(request)
    return redirect("user:index")

# ログインしていないと実行できず404エラーとなる
@login_required
def info(request):
    return HttpResponse("ログインしています。")
