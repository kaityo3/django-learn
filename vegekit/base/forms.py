from django import forms
# getusermodel->今使用しているusermodelを自動的に持ってくる->import userとする必要がなくなる
# 上の設定はsettings.py　→ AUTH_USER_MODELで定義される
from django.contrib.auth import get_user_model
 

# userを作成するフォームの作成->user作成のページを作成する際にviewで呼び出される
class UserCreationForm(forms.ModelForm):
    password = forms.CharField()
 
    class Meta:
        # userモデルがmodelに代入される
        model = get_user_model()
        fields = ('username', 'email', 'password', )
 
    # オーバーライドして記述→不正なパスワードがないか検知
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user