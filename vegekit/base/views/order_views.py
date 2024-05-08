from django.views.generic import ListView ,DetailView
from base.models import Order
import json
# loginしていないとそのviewを返さないようにする
from django.contrib.auth.mixins import LoginRequiredMixin

# 振り返りだが、基本的にviews.pyからはobjectという名前でhtmlにデータが渡される

# 注文履歴一覧
class OrderIndexView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'pages/orders.html'
    # created_atをもとに並び替える(-を先頭に付けると降順になる)
    ordering = '-created_at'
 
    # そのままでは、全員の注文履歴を表示することが出来てしまうため
    # 以下モジュールをオーバーライドして、自分の履歴のみを引っ張ってくる
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
 
 
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'pages/order.html'
    
    # ＊get_querysetメソッドの追記
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
 
    # 以下モジュールをオーバーライドしている
    # 
    def get_context_data(self, **kwargs):
        # 既存の処理は引き継いでおく
        context = super().get_context_data(**kwargs)
        # 現在読み込まれている1つの注文情報をobjとして読み込む
        # 保存している段階ではjsonファイルとなってしまっているので、json.loadで辞書型に変換している
        obj = self.get_object()
        # itemとshipping情報については個別に追加する
        context["items"] = json.loads(obj.items)
        context["shipping"] = json.loads(obj.shipping)
        return context