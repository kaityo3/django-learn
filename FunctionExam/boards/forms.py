from django import forms
from .models import Themes, Comments

class Theme_form(forms.ModelForm):
    title = forms.CharField(label="テーマ")

    class Meta:
        model = Themes
        fields = ("title",)
        
# 以下作成してみたが、よく考えたら上と同じ
class ThemeEditForm(forms.ModelForm):
    title = forms.CharField(label="テーマ")

    class Meta:
        model = Themes
        fields = ("title",)

# class DeleteThemeForm(forms.Form):
#     id = forms.IntegerField(widget=forms.HiddenInput)
class DeleteThemeForm(forms.ModelForm):
    class Meta:
        model=Themes
        fields = []

class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(label="",widget=forms.Textarea(attrs={"rows":5,"cols":60}))
    class Meta:
        model=Comments
        fields = ("comment",)

