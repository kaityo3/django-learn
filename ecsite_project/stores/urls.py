from django.urls import path
from .views import (
    ProductListView, ProductDatailView, add_product, CartItemsView,
    CartUpdateView, CartDeleteView,
)

app_name = "stores"
urlpatterns=[
    path("product_list/", ProductListView.as_view(),name="product_list"),
    path("product/<int:pk>", ProductDatailView.as_view(),name="product"),
    path("add_product/", add_product,name="add_product"),
    path("cart_items/", CartItemsView.as_view(),name="cart_items"),
    path("update_cart/<int:pk>", CartUpdateView.as_view(),name="update_cart"),
    path("delete_cart/<int:pk>", CartDeleteView.as_view(),name="delete_cart"),
]
