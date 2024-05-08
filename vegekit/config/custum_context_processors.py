# 共通の変数を定義する(viewで何度も渡している値を統一するイメージ)
# settings.TITLEするためのimport
from django.conf import settings
from base.models import Item
 
# ここで渡す値はわざわざviewを通す必要がない

def base(request):
    items = Item.objects.filter(is_published=True)
    # 辞書を返す
    return {
        # サイトのタイトル
        'TITLE': settings.TITLE,
        # カートのページ、アイテムページなどで追加のアイテムを促したい際、簡単にそのitemを渡せるようにする
        'ADDTIONAL_ITEMS': items,
        # 人気のアイテム(itemを販売数で降順にしたもの)
        'POPULAR_ITEMS': items.order_by('-sold_count')
    }