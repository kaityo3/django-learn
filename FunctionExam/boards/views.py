from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Themes, Comments
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse


def create_theme(request):
    create_theme_form = forms.Theme_form(request.POST or None)
    if create_theme_form.is_valid():
        # formからformに入っているinstanceを呼び出して任意に書き換える
        create_theme_form.instance.user = request.user
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

def edit_theme(request, id):
    theme = get_object_or_404(Themes,pk=id)
    # themeの持つ編集者のidとログイン中userのidが異なる場合は404エラーを出す
    if theme.user.id != request.user.id:
        raise Http404
    
    # Theme_formを流用可能
    theme_edit_form = forms.Theme_form(data = request.POST or None, instance=theme)
    if theme_edit_form.is_valid():
        theme_edit_form.save()
        messages.success(request,"タイトル修正が完了しました")
        return redirect('boards:list_themes')

    return render(
        request,
        "boards/edit_theme.html",
        context={
            "id": id,
            "theme_edit_form": theme_edit_form,  
        }
    )


def delete_theme(request, id):
    theme = get_object_or_404(Themes,pk=id)
    if theme.user.id != request.user.id:
        raise Http404
    
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    # 値はないが、csrfのチェックのためにis_valid()を実施する
    if delete_theme_form.is_valid():
        theme.delete()
        messages.success(request,"掲示板削除が完了しました。")
        return redirect('boards:list_themes')

    return render(
        request,
        "boards/delete_theme.html",
        context={
            "theme": theme,
            "delete_theme_form": delete_theme_form,
        }
    )

def post_comments(request, theme_id):
    saved_comment = cache.get(f"saved_comment-theme_id={theme_id}-user_id={request.user.id}", "")
    post_comment_form = forms.PostCommentForm(request.POST or None, initial={"comment": saved_comment})
    theme = get_object_or_404(Themes,pk=theme_id)
    comments = Comments.objects.fetch_by_theme_id(theme)

    if post_comment_form.is_valid():
        if not request.user.is_authenticated:
            print("認証されてない")
            raise Http404
        post_comment_form.instance.theme = theme
        post_comment_form.instance.user = request.user
        post_comment_form.save()
        cache.delete(f"saved_comment-theme_id={theme_id}-user_id={request.user.id}")
        return redirect('boards:post_comments',theme_id=theme_id)
    
    return render(
        request,
        "boards/post_comments.html",
        context={
            "theme": theme,
            "post_comment_form": post_comment_form,
            "comments": comments,
        }
    )

def save_comment(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment = request.GET.get("comment")
        theme_id = request.GET.get("theme_id")
        if comment and theme_id:
            cache.set(f"saved_comment-theme_id={theme_id}-user_id={request.user.id}", comment)
            return JsonResponse({
                "message": "一時保存しました"
            })


