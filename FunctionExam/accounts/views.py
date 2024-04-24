from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(
        request,
        "accounts/home.html"
    )

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    # print(type(regist_form))
    # print(dir(regist_form))
    # print("*"*80)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('accounts:home')
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(
        request, 'accounts/regist.html', context={
            'regist_form': regist_form,
        }
    )

def activate_user(request, token):
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
    return render(
        request,
        "accounts/activate_user.html"
    )

def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get("email")
        password = login_form.cleaned_data.get("password")
        # ユーザーが存在しかつパスワードが正しいかチェック
        user = authenticate(email=email,password=password)
        print(user)
        if user:
            # "is_active"は関数ではなく単なるbool値を持つ変数なので括弧は不要
            if user.is_active:
                login(request, user)
                messages.success(request,"ログインが完了しました")
                return redirect("accounts:home")
            else:
                messages.warning(request,"ユーザーがアクティブじゃないです")
        else:
            messages.warning(request,"ユーザーかパスワードが間違ってます")
    return render(
        request,
        "accounts/user_login.html",
        context={
            "login_form": login_form
        }
    )

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,"ログアウトしました")
    return redirect("accounts:home")
