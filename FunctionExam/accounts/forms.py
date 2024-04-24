from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password


class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())
    
    class Meta():
        model = Users
        fields = ('username', 'age', 'email', 'password')
    
    def clean(self):
        # super().clean()によってdjango基本機能でパスワードをバリデート
        cleaned_data = super().clean()
        # その後、confirmと照らし合わせ、違った場合のみエラーを出力する
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    # この関数定義がないと、passwordのバリデーションと暗号化がなされない
    def save(self, commit=False):
        user = super().save(commit=False)
        # print(type(user))
        # print(dir(user))
        print(user.password)
        validate_password(self.cleaned_data['password'], Users)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user



class LoginForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)

