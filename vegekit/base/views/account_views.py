# django標準の新規作成と更新のviewをimport
from django.views.generic import CreateView, UpdateView
# login画面のview
from django.contrib.auth.views import LoginView
# ログインしていないと表示させてはいけないページについて、制御を実施する
from django.contrib.auth.mixins import LoginRequiredMixin
# userモデルを自動的にimportする(import userとする必要がない)
from django.contrib.auth import get_user_model
#ユーザー定義のdbフォーム
from base.models import Profile
from base.forms import UserCreationForm
# 登録完了の際に出力するメッセージ
from django.contrib import messages

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView

 

# 新規登録のページ
class SignUpView(CreateView):
    # userフォームのクラスを渡すことによってうまく機能する(forms.pyは必須)
    form_class = UserCreationForm
    # idが作成できた後のページ
    success_url = '/login/'
    #表示するページ
    template_name = 'pages/login_signup.html'
    
    # アカウント作成に成功したら、遷移後のページでメッセージを出力する
    # form_valid:formが有効であるか検証されて、有効であった場合の処理が入る→そのためのformファイル...?
    def form_valid(self, form):
        messages.success(self.request, 'ユーザー作成に成功しました。続けてログインしてください。')
        return super().form_valid(form)
 
# ログインページ
# LoginViewなどとすると継承する親との関係が分かりづらいため、今回のみLoginという名前
class Login(LoginView):
    template_name = 'pages/login_signup.html'
    
    # 特にカスタマイズせず
    def form_valid(self, form):
        messages.success(self.request, 'ログインしました。')
        return super().form_valid(form)
 
    # 特にカスタマイズせず
    def form_invalid(self, form):
        messages.error(self.request, 'ログイン出来ませんでした')
        return super().form_invalid(form)
 
 
# アカウントのコアな情報の更新
# loginしていないと参照できないよう、LoginRequiredMixinを追加(引数の先頭に追加する)
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ('username', 'email',)
    # 更新後も同様のページに残る
    success_url = '/account/'
 
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得(getは「?」以降のurlの文字を使用するのが一般的か)
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

# パスワード変更view
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    model = get_user_model()
    template_name = 'pages/passwdChg.html'
    success_url = '/'
    
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得(getは「?」以降のurlの文字を使用するのが一般的か)
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

    def form_valid(self, form):
        messages.success(self.request, 'パスワードを変更しました。')
        return super().form_valid(form)



# AccountUpdateViewとほぼ同様
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    fields = ('name', 'zipcode', 'prefecture',
              'city', 'address1', 'address2', 'tel')
    success_url = '/profile/'
 
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()