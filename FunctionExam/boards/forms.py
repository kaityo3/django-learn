from django import forms
from .models import Themes, Comments

class Theme_form(forms.ModelForm):
    title = forms.CharField(label="テーマ")

    class Meta:
        model = Themes
        fields = ("title",)
