from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm

# class UserLoginView(FormView):
#     template_name = "user_login.html"
#     form_class = UserLoginForm

#     def post(self, request, *args, **kwargs):
        
#         email = request.POST["email"]
#         password = request.POST["password"]
#         # ユーザーが存在しかつパスワードが正しいかチェック
#         user = authenticate(username=email,password=password)
#         next_url = request.POST["next"]
#                 # もし正しかった場合
#         if user:
#             # "is_active"は関数ではなく単なるbool値を持つ変数なので括弧は不要
#             if user.is_active:
# 		            # ログイン出来る
#                 login(request, user)
#                 if next_url:
#                     return redirect(next_url)
#                 else:
#                    return redirect("accounts:home")
#             else:
#                 return HttpResponse("アカウントがアクティブでないです")
#         else:
#             return HttpResponse("ユーザーが存在しません")

class UserLoginView(LoginView):
    template_name = "user_login.html"
    authentication_form = UserLoginForm

    # formの値検証で呼び出される関数のオーバーライド
    def form_valid(self, form):
        remember = form.cleaned_data["remember"]
        if remember:
            self.request.session.set_expiry(36000)
        return super().form_valid(form)

# class UserLogoutView(View):
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect("accounts:home")

class UserLogoutView(LogoutView):
    pass


# LoginRequiredMixinはデフォルトのリダイレクト先がlogin/
class UserView(LoginRequiredMixin, TemplateView):
    template_name = "user.html"

# @method_decorator(login_required, name="dispatch")
# class UserView(TemplateView):
#     template_name = "user.html"

#     # dispatch関数(get,postのどちらを実行するか切り分ける関数)を明示的に記載して、その上にdecoratorを配置する。
#     # @method_decorator(login_required)
#     def dispatch(self, *args: Any, **kwargs: Any):
#         return super().dispatch(*args, **kwargs)
