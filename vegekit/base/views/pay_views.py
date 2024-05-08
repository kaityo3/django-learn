from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
from stripe.api_resources import tax_rate
from base.models import Item, Order
import stripe
# ログインしていないと表示させてはいけないページについて、制御を実施する
from django.contrib.auth.mixins import LoginRequiredMixin
# djangoをjsonに直してくれるコンポーネント
from django.core import serializers
import json
# messages
from django.contrib import messages


stripe.api_key = settings.STRIPE_API_SECRET_KEY

# stripe標準のモジュール(taxrateを使用して作成している)
tax_rate = stripe.TaxRate.create(
    display_name="消費税",
    description="消費税",
    country="JP",
    jurisdiction="JP",  # 管轄を指定
    # settingsにて設定した税率を適用している
    percentage=settings.TAX_RATE * 100,  # 10%
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)
#  決済完了ページ

class PaySuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/success.html'
 
    def get(self, request, *args, **kwargs):
        # orderオブジェクト(現在のuserのみ)の最新のもの(作成日降順の一番上)を取得
        order = Order.objects.filter(
            user=request.user).order_by('-created_at')[0]
        # confirmについて注文確定に変更
        order.is_confirmed = True
        # saveを実施
        order.save()

        # 決済完了後、カート情報は削除する
        del request.session['cart']
 
        return super().get(request, *args, **kwargs)
 
# 決済キャンセルページ 
class PayCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/cancel.html'
 
    def get(self, request, *args, **kwargs):
        # orderオブジェクト(現在のuserのみ)の最新のもの(作成日降順の一番上)を取得
        order = Order.objects.filter(
            user=request.user).order_by('-created_at')[0]

        # 在庫数と販売数を元の状態に戻す
        # for文でitemsの中身をロード(キー情報を使う)
        for elem in json.loads(order.items):
            # キーをもとに、Itemsモデルの方のitemを取得して
            item = Item.objects.get(pk=elem['pk'])
            # 今回の注文を取り消すように販売量と在庫数の情報を更新する
            item.sold_count -= elem['quantity']
            item.stock += elem['quantity']
            item.save()

        # is_confirmedがFalseであれば削除（仮オーダー削除）
        if not order.is_confirmed:
            order.delete()
 
        return super().get(request, *args, **kwargs)
 

 
# stripeの仕様通りに、設計すべき部分
#商品毎のデータをreturnとして返し、stripe側で処理してもらえる形になっている
def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            # 日本円
            'currency': 'jpy',
            # 商品の単価
            'unit_amount': unit_amount,
            # 商品名
            'product_data': {'name': name, },
        },
        # 商品在庫量
        'quantity': quantity,
        # 税金(tax_rateという変数については1つ上で定義済)
        "tax_rates": [tax_rate.id],
    }
 

# PayWithStripeでちゃんと住所が入力されているか確認する
# どれか一つでも欠けていたらFalseを出力
def check_profile_filled(profile):
    if profile.name is None or profile.name == '':
        return False
    elif profile.zipcode is None or profile.zipcode == '':
        return False
    elif profile.prefecture is None or profile.prefecture == '':
        return False
    elif profile.city is None or profile.city == '':
        return False
    elif profile.address1 is None or profile.address1 == '':
        return False
    return True


# django(View)はpost,get等毎に機能を実装できる
# paywithstripeはstripeから読み込まれるページ
class PayWithStripe(LoginRequiredMixin, View):
 
    def post(self, request, *args, **kwargs):
        # プロフィールが埋まっているか確認
        if not check_profile_filled(request.user.profile):
            # なぜプロフィールに飛ばされたかメッセージを表示
            messages.warning(request, 'プロフィール情報に漏れがあります')
            return redirect('/profile/')

        # 現在のcartの情報を取得する
        cart = request.session.get('cart', None)
        # cart情報がなければtopページに戻す
        if cart is None or len(cart) == 0:
            messages.warning(request, 'カートに商品を追加してください')
            return redirect('/')
 
        items = [] #Orderモデル用に追記

        # itemの情報をline_itemに全てforで取り出す
        line_items = []
        for item_pk, quantity in cart['items'].items():
            # Itemの参照先はItemモデル(データベース)
            item = Item.objects.get(pk=item_pk)
            # stripeの決済ページ(以下checkout_session)に表示する内容をこの関数で作っている(関数は上で定義済)
            line_item = create_line_item(
                item.price, item.name, quantity)
            line_items.append(line_item)

            #Orderモデル用に追記
            # itemsリストに辞書型でItemのデータを保存している
            items.append({
                'pk': item.pk,
                'name': item.name,
                'image': str(item.image),
                'price': item.price,
                'quantity': quantity,
            })

            # 在庫をこの時点で引いておき、注文キャンセルの場合はもとに戻す
            # 販売数も加算しておく
            item.stock -= quantity
            item.sold_count += quantity
            # 保存することでデータベースも更新される
            item.save() 

        # 仮注文を作成(is_confirmed = true)
        # orderモデルに1つのorder情報を作成する
        Order.objects.create(
            # 現在のuser情報とid
            user=request.user,
            uid=request.user.pk,
            # orderモデル用に上で作成したitemsをjson形式で代入する
            items=json.dumps(items),
            # user.profileはデータベース形式のため、itemsとは違いdjangoの機能でjsonファイルに変換している
            shipping=serializers.serialize("json", [request.user.profile]),
            amount=cart['total'],
            tax_included=cart['tax_included_total']
        )
 
        # 決済ページの定義、stripeの機能を使って決済ページを生成
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
        
            # 決済後のページ定義　
            # stripeの都合上、フルでurlが必要なため、my_urlとして定義した部分を引っ張ってきている
            success_url=f'{settings.MY_URL}/pay/success/',
            cancel_url=f'{settings.MY_URL}/pay/cancel/',
        )
        return redirect(checkout_session.url)