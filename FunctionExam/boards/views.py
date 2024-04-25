from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from .models import Themes

def create_theme(request):
    create_theme_form = forms.Theme_form(request.POST or None)
    if create_theme_form.is_valid():
        create_theme_form.instance.user = request.user
        # create_theme_form.user = request.user
        messages.success(request,"掲示板を作成しました。")
        create_theme_form.save()
        return redirect('boards:list_themes')
    return render(
        request,
        "boards/create_theme.html",
        context={
            "create_theme_form": create_theme_form,
        }
    )

def list_themes(request):
    themes = Themes.objects.fetch_all_themes()
    return render(
        request,
        "boards/list_themes.html",
        context={
            "themes": themes,
        }
    )
