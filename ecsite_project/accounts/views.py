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


class UserLoginView(LoginView):
    template_name = "user_login.html"
    authentication_form = UserLoginForm

    # formの値検証で呼び出される関数のオーバーライド
    def form_valid(self, form):
        remember = form.cleaned_data["remember"]
        if remember:
            self.request.session.set_expiry(36000)
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


# LoginRequiredMixinはデフォルトのリダイレクト先がlogin/
class UserView(LoginRequiredMixin, TemplateView):
    template_name = "user.html"
