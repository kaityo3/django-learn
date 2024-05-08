from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.base import(
    View, TemplateView, RedirectView
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView, FormView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import Http404

from . import forms
from .models import Books, Pictures
from datetime import datetime
from django.urls import reverse_lazy, reverse
import logging

application_logger = logging.getLogger("application-logger")
error_logger = logging.getLogger("error-logger")

class IndexView(View):
    # classed viewはgetとpostをオーバーライドする形で作成する
    def get(self, request, *args, **kwargs):
        bookform = forms.BookForm(request.POST or None)
        return render(
            request,
            "index.html",
            context={
                "bookform": bookform,
            }
        )
    
    def post(self, request, *args, **kwargs):
        bookform = forms.BookForm(request.POST or None)
        if bookform.is_valid():
            bookform.save()
        return render(
            request,
            "index.html",
            context={
                "bookform": bookform,
            }
        )

class HomeView(TemplateView):

    template_name = "home.html"
    
    # contextを渡したい場合、get_context_dateメソッドを上書きする。
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        # print(kwargs)
        application_logger.debug("Home画面を表示します")
        if kwargs.get("name") == "あああ":
            # error_logger.error("この名前は使用できません")
            raise Http404("この名前は使用できません。")

        context["name"] = kwargs.get("name")
        context["time"] = datetime.now()
        return context
    
class BookDetailView(DetailView):
    model = Books
    template_name = "book.html"

    # modelで指定したデータがhtml側で"object.変数名"とし取得可能
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        print(context)
        context["form"] = forms.BookForm()
        return context

class BookListView(ListView):
    model = Books
    template_name = "book_list.html"

    # 順番を並べ替えたい場合
    def get_queryset(self):
        qs = super(BookListView, self).get_queryset()
        if "name" in self.kwargs:
            qs = qs.filter(name__startswith = self.kwargs["name"])
        qs = qs.order_by("-id")
        # print(qs)
        return qs

class BookCreateView(CreateView):
    model = Books
    fields = ["name","description","price"]
    template_name = "add_book.html"
    # success_url = reverse_lazy("store:book_list")

    # おそらくform_validは上位の処理でis_validが実行されて問題ない場合に呼び出されている
    # 上位ではmodelの保存に使用されている
    def form_valid(self, form):
        # 値の定義
        form.instance.create_at = datetime.now()
        form.instance.update_at = datetime.now()
        # (form.save())を上位メソッドにて呼び出し
        return super(BookCreateView, self).form_valid(form)
    
    def get_initial(self, **kwargs):
        initial = super(BookCreateView, self).get_initial(**kwargs)
        initial["name"] = "sample"
        return initial

class BookUpdateView(SuccessMessageMixin, UpdateView):
    
    template_name = "update_book.html"
    model = Books
    form_class = forms.BookUpdateForm
    success_message = '更新に成功しました'
    
    def get_success_url(self):
        # print(self.object.pk)
        return reverse("store:edit_book", kwargs={'pk': self.object.id})
    
    def get_success_message(self, cleaned_data):
        # print(cleaned_data)
        return cleaned_data.get("name")+"を更新しました。"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        picture_form = forms.PictureUploadForm
        pictures = Pictures.objects.filter_by_book(book=self.object)
        context["pictures"] = pictures
        context["picture_form"] = picture_form
        return context

    def post(self, request, *args, **kwargs):
        picture_form = forms.PictureUploadForm(request.POST or None, request.FILES or None)
        if picture_form.is_valid and request.FILES:
            # print(dir(self))
            # 更新中のbook objectの登録
            book = self.get_object()
            # bookを引数で指定→formsのsaveメソッドへ
            picture_form.save(book=book)

        # Books modelの保存処理は以下superで実行される
        return super().post(request, *args, **kwargs)
    
class BookDeleteView(DeleteView):

    template_name = "delete_book.html"
    model = Books
    success_url = reverse_lazy("store:book_list")


class BookFormView(FormView):

    model = Books
    form_class = forms.BookForm
    template_name = "form_book.html"
    success_url = reverse_lazy("store:book_list")

    def get_initial(self, **kwargs):
        initial = super(BookFormView, self).get_initial(**kwargs)
        initial["name"] = "sample"
        return initial

    def form_valid(self, form):
        # 値の定義
        form.save()
        return super(BookFormView, self).form_valid(form)

class BookRedirectView(RedirectView):
    # url = "https://google.com"
    def get_redirect_url(self, *args, **kwargs):
        book = Books.objects.first()
        if "pk" in kwargs:
            return reverse("store:detail_book", kwargs={"pk": kwargs["pk"]})
        print(book)
        return reverse("store:edit_book", kwargs={"pk": book.pk})

def delete_picture(request, pk):
    picture = get_object_or_404(Pictures, pk=pk)
    picture.delete()

    # データベースと同時にファイルそのものを消したい場合
    # import os
    # if os.path.isfile(picture.picture.path):
    #     os.remove(picture.picture.path)

    messages.success(request, "画像を削除しました")
    return redirect("store:edit_book", pk=picture.book.id)
