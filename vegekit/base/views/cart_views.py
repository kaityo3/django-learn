from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import ListView ,View
from base.models import Item
from collections import OrderedDict
# ログインしていないと表示させてはいけないページについて、制御を実施する
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class CartListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/cart.html'

    # get_querysetはListViewから継承したメソッド
    # querysetとは今だとitemインスタンスがリストになったもの。それをこちら側で書き換える
    def get_queryset(self):
        # cart情報がある場合変数に代入、なければNone
        cart = self.request.session.get('cart', None)
        #もしなければトップページにリダイレクトする
        if cart is None or len(cart) == 0:
            return redirect('/')
        # もしcartがあった場合
        #初期化メソッド
        #self.quwrysetは元々公式に存在する変数で上書きしているもの
        self.queryset = []
        self.total = 0
        # cartの中にadd_cart_viewで追加したsession['cart']が存在するのは明らか
        #.items()でkeyとvalueを両方取り出せる
        for item_pk, quantity in cart['items'].items():
            obj = Item.objects.get(pk=item_pk)
            # dbの定義には必要ない一時的な合計金額等は変数として保存
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            # 処理したitemインスタンスを上で初期化しているquerysetリストに追加する
            self.queryset.append(obj)
            # 税抜価格をtotalにどんどん追加する
            self.total += obj.subtotal
        # import settinngをしており、その設定値によってTAX_RATEが決まり税込み金額が計算される
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        # cartインスタンスの中にこれら合計値等を追加する
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        # cartの内容を上書きする
        self.request.session['cart'] = cart
        # listviewのquerysetを返す
        # self.queryset()はそのそも存在するため親の機能として、session等を返してくれる
        return super().get_queryset()

    # これも親クラスが持っている関数をオーバーライドしている
    # object_listはこのcontextデータで定義できていた
    def get_context_data(self, **kwargs):
        #親のcontextを実行
        context = super().get_context_data(**kwargs)
        # contextの新しいキー'total','tax_included_total'を追加する
        #そうすることで、cart.htmlの中以下total,tax~,に変数が代入できるようになる
        # cart.html
        # <p>小計 - ¥{{total}}</p>
        # <p>税込計 - ¥{{tax_included_total}}</p>
        try:
            context["total"] = self.total
            context["tax_included_total"] = self.tax_included_total
        except Exception:
            pass
        return context

# index.html中にあるフォームから渡されたデータを処理してhtmlを生成
# index.html
        # <form action="/cart/add/" method="POST" class="">
        #   {% csrf_token %}
        #   <!-- どのitemか -->
        #   <input type="hidden" name="item_pk" value="{{object.pk}}">
        #   <p>
        #     <!-- 数量を指定するフォーム -->
        #     <input type="number" class="form-control d-inline w-25" name="quantity" value="1" max="{{object.stock}}"> 点
        #   </p>
class AddCartView(LoginRequiredMixin, View):
    # postメソッドで送信されてきたviewの処理をここに書ける(getも同様)
    def post(self, request):
        # postの中身の変数に代入する
        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        #sessionの中のcartを持ってくる、なければnoneを返す
        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            # 辞書型配列で追加した順番を意識するため、orderedDice(順序付き辞書)を指定している
            items = OrderedDict()
            # 辞書型のcartに{キーitems,orderdict型item}が代入
            cart = {'items': items}
        # もし、上で定義したcartのitemsにitem_pk(itemのid)があれば(既にカート中に同一itemがあれば)
        if item_pk in cart['items']:
            #そのitemにitemの量を追加する
            cart['items'][item_pk] += quantity
        # まだカートにアイテムがなければ注文数量をそのまま代入する
        else :
            cart['items'][item_pk] = quantity
        # 最後にrequest.sessionにcartの中身を代入する
        # この時はpython辞書型の追加と同様、もし'cart'keyが無ければ勝手に作成される
        request.session['cart'] = cart
        #処理が終わったら、cartのページにリダイレクトさせる
        return redirect('/cart/')

# 1つ下の関数を実施するにあたり、loginが必須となるようにするデコレータ
@login_required
# requestとpk(item_idを引数)
def remove_from_cart(request, pk):
    cart = request.session.get('cart', None)
    # もし、cardの中がNoneじゃないなら、item[pk]を消去しcartを再代入する
    if cart is not None:
        del cart['items'][pk]
        request.session['cart'] = cart
    return redirect('/cart/')

