from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    UpdateView, DeleteView, CreateView,
)
from django.urls import reverse_lazy


from .models import Products, Carts, CartItems
from .forms import CartUpdateForm

import os



class ProductListView(LoginRequiredMixin, ListView):
    model = Products
    template_name = os.path.join("stores", "product_list.html")

    # 入力されたデータによって、取得するクエリを絞り込む
    def get_queryset(self):
        query = super().get_queryset()
        product_type_name = self.request.GET.get('product_type_name', None)
        product_name = self.request.GET.get('product_name', None)

        if product_type_name:
            # product_typeのnameについて絞り込める
            # icontains	指定した文字列を含んでいる場合(大文字小文字を区別しない)
            query = query.filter(product_type__name__icontains=product_type_name)
        if product_name:
            query = query.filter(name__icontains=product_name)

        order_by_price = self.request.GET.get('order_by_price', None)
        if order_by_price == "1":
            query = query.order_by("price")
        elif order_by_price == "2":
            query = query.order_by("-price")

        return query

    # 検索窓に検索した文字列を残すための機能
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_type_name"] = self.request.GET.get('product_type_name', "")
        context["product_name"] = self.request.GET.get('product_name', "")
        context["order_by_price"] = self.request.GET.get('order_by_price', "")
        return context
    

class ProductDatailView(LoginRequiredMixin, DetailView):
    model = Products
    template_name = os.path.join("stores", "product.html")

    def get_context_data(self, **kwargs):
        # print(kwargs)
        context = super().get_context_data(**kwargs)
        context['is_added'] = CartItems.objects.filter(
            cart_id=self.request.user.id,
            product_id=kwargs.get('object').id
        ).first()
        return context



@login_required
def add_product(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        product = get_object_or_404(Products, id=product_id)
        if int(quantity) > product.stock:
            response = JsonResponse({"message": "在庫数を超えています。"})
            response.status_code = 403
            return response
        if int(quantity) <= 0:
            response = JsonResponse({"message": "0より大きい値を入力してね"})
            response.status_code = 403
            return response
        cart = Carts.objects.get_or_create(
            user = request.user
        )
        if all([product_id, cart, quantity]):
            CartItems.objects.save_item(
                quantity = quantity,
                product_id = product_id,
                # get_or_createの際、タプル型でデータが返るため
                cart = cart[0],
            )
            return JsonResponse({"message": "商品をカートに追加しました。"})


class CartItemsView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join("stores", "cart_items.html")


    # ここの処理managerクラスにした方がいいのでは？
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        # query = CartItems.object.get_items()
        query = CartItems.objects.filter(cart_id=user_id)
        total_price = 0
        items = []
        for item in query.all():
            sub_total = item.quantity * item.product.price
            # pictureインスタンスを取得
            picture_ins = item.product.productpictures_set.first()
            # インスタンスにデータがあればpictureにセット、なければNone
            picture = picture_ins.picture if picture_ins else None
            # 指定量より在庫が多ければTrue,無ければFalse
            in_stock = True if item.product.stock >= item.quantity else False
            print(in_stock,item.product.name)
            tmp_item = {
                "quantity": item.quantity,
                "picture": picture,
                "name": item.product.name,
                "id": item.id,
                "price": item.product.price,
                "in_stock": in_stock,
                "sub_total": sub_total
            }
            items.append(tmp_item)
            total_price += sub_total
        context["total_price"] = total_price
        context["items"] = items

        return context

# おそらくajaxで通信可能
class CartUpdateView(LoginRequiredMixin, UpdateView):
    template_name = os.path.join('stores', 'update_cart.html')
    form_class = CartUpdateForm
    model = CartItems
    success_url = reverse_lazy('stores:cart_items')

# おそらくajaxで通信可能
class CartDeleteView(LoginRequiredMixin, DeleteView):
    template_name = os.path.join('stores', 'delete_cart.html')
    model = CartItems
    success_url = reverse_lazy('stores:cart_items')
