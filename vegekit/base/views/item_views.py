from django.shortcuts import render
from django.views.generic import ListView ,DetailView
from base.models import Item, Category, Tag


class IndexListView(ListView):
    #djangoのlistviewの機能で、modelを指定するとlistが表示される
    #template nameにItemの内容を全て"object_list"として変数を渡す
    model = Item
    template_name = 'pages/index.html'

""" 以下上のクラスを関数で記述した場合
def index(request):
    #Itemから全てのオブジェクトをリストとして持ってくる
    object_list = Item.objects.all()
    #contextとしてley,valueの形で変数に代入する
    context = {
        'object_list':object_list,
    }
    #rewuestに関して、contextを引数にhtml情報を返す
    return render(request,'pages/index.html',context) """

class ItemDetailView(DetailView):
    #"DetailView"は個別のItemのインスタンスを変数"object"として渡す(object_listはインスタンス全てが渡る)
    model = Item
    template_name = 'pages/item.html'

class CategoryListView(ListView):
    model = Item
    # tagやカテゴリを持っているItem一覧を表示する
    template_name = 'pages/list.html'
    # 1ページに幾つのアイテムを表示するか
    paginate_by = 2
 
    # オーバーライド
    def get_queryset(self):
        # slug(カテゴリのid) = 選択したtagのidのデータを引っ張ってくる
        self.category = Category.objects.get(slug=self.kwargs['pk'])
        # objectにフィルタして、公開されているかつ、categoryで選択したobjectを「Item」モデルから返す
        return Item.objects.filter(is_published=True, category=self.category)
 
    # オーバーライド
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # htmlに返す値を追加する(今回はカテゴリ名)
        context['title'] = f'Category #{self.category.name}'
        return context

# タグについてもカテゴリと同様
class TagListView(ListView):
    # tagやカテゴリを持っているItem一覧を表示する
    model = Item
    template_name = 'pages/list.html'
    # 1ページに幾つのアイテムを表示するか
    paginate_by = 2
 
    # オーバーライド
    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(is_published=True, tags=self.tag)
    
    # オーバーライド
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Tag #{self.tag.name}"
        return context
