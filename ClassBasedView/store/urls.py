from django.urls import path
from .views import (
    IndexView, HomeView, BookDetailView, BookListView, 
    BookCreateView, BookUpdateView, BookDeleteView, 
    BookFormView, BookRedirectView, delete_picture
)
from django.views.generic.base import TemplateView, RedirectView

app_name = "store"

urlpatterns = [
    # viewsで定義したclass.as_view()で参照可能
    path("index/", IndexView.as_view(),name="index"),
    # path("home/", TemplateView.as_view(template_name="home.html"),name="home"),
    path("", HomeView.as_view(),name="home"),
    path("detail_book/<int:pk>", BookDetailView.as_view(),name="detail_book"),
    path("book_list/", BookListView.as_view(),name="book_list"),
    path("book_list/<name>", BookListView.as_view(),name="book_list"),
    path("add_book/", BookCreateView.as_view(),name="add_book"),
    path("edit_book/<int:pk>", BookUpdateView.as_view(),name="edit_book"),
    path("delete_book/<int:pk>", BookDeleteView.as_view(),name="delete_book"),
    path("form_book/", BookFormView.as_view(),name="form_book"),
    path("google/", RedirectView.as_view(url="https://google.com"),name="form_book"),
    path("redirect_book/", BookRedirectView.as_view(),name="redirect_book"),
    path("redirect_book/<int:pk>", BookRedirectView.as_view(),name="redirect_book"),
    path("delete_picture/<int:pk>", delete_picture,name="delete_picture"),
]
