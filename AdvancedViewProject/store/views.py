from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from .models import Items
from django.http import Http404

def index(request):
    return render(request, "store/index.html")

def item_list(request):
    items = Items.objects.all()
    # items = get_list_or_404(Items, pk__gt=4)
    return render(
        request, 
        "store/item_list.html",
        context={
            "items": items,
        }
    )

def item_detail(request, id):
    if id == 0:
        raise Http404
    # filterで値を取り出す際はリストで取り出されるためfirst()でリストから抜き出す必要あり
    # item = Items.objects.filter(id=id).first()

    # getで取得しようとすると、itemがない場合に即時500エラーとなってしまう
    # item = Items.objects.get(id=id)
    
    # getで値が歩かないか確認し、無ければ404エラーを返す。(pk以外にも絞り込みは可能→get_object_or_404(Items,pk=id ,name="リンゴ"))
    item = get_object_or_404(Items,pk=id)
    if item is None:
        return redirect("store:item_list")

    return render(
        request,
        "store/item_detail.html",
        context={
            "item": item
        }
    )

def to_google(request):
    return redirect("https://www.google.com")

def one_item(request):
    return redirect("store:item_detail", id=1)

def page_not_found(request, exception):
    return render(
        request,
        "store/404.html",
        status=404
    )
    # return redirect("srore:item_list")

def server_error(request):
    return render(
        request,
        "store/500.html",
        status=500
    )
