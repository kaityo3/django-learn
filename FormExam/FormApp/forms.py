from django import forms
from .models import Students

class StudentForm(forms.ModelForm):
    name = forms.CharField(label="名前")
    age = forms.IntegerField(label="歳")
    grade = forms.IntegerField(label="学年")
    picture = forms.FileField(label="ファイルアップロード")
    class Meta:
        model = Students
        fields = "__all__"

class StudentUpdateForm(forms.Form):
    name = forms.CharField(label="名前")
    age = forms.IntegerField(label="歳")
    grade = forms.IntegerField(label="学年",required=False)
    picture = forms.FileField(label="ファイルアップロード",required=False)

class StudentDeleteForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
