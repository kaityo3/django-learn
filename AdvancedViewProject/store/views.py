from django.shortcuts import render,redirect
from .models import Items

def index(request):
    return render(request, "store/index.html")

def item_list(request):
    items = Items.objects.all()
    return render(
        request, 
        "store/item_list.html",
        context={
            "items": items,
        }
    )

def item_detail(request, id):
    # filterで値を取り出す際はリストで取り出されるためfirst()でリストから抜き出す必要あり
    item = Items.objects.filter(id=id).first()
    # getで取得しようとすると、itemがない場合に即時エラーとなってしまうためfilterが適切
    # item = Items.objects.get(id=id)
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
