from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

# 現在djangoで使用しているUserのモデルが返る
Users=get_user_model()

class RegistForm(forms.ModelForm):
    username = forms.CharField(label="名前")
    age = forms.IntegerField(label="年齢", min_value=0)
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Password再入力", widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ("username","email","password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("パスワードが一致しません")
        
    def clean_password(self):
        cleaned_data = super().clean()
        cleaned_password = self.cleaned_data.get("password")
        try:
            validate_password(cleaned_password)
        except ValidationError as e:
            raise e
        return cleaned_password

    
    def save(self, commit=False):
        user = super().save(commit=False)
        # 暗号化処理

        validate_password(self.cleaned_data["password"], user)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user

# class UserLoginForm(forms.Form):
#     email = forms.EmailField(label="メールアドレス")
#     password = forms.CharField(label="password", widget=forms.PasswordInput)

class UserLoginForm(AuthenticationForm):
    # username →models.pyの"USERNAME_FIELD"にあたるもの
    username = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    remember = forms.BooleanField(label="ログイン状態を保持する", required=False)
