import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Students

# 全件取得
print(Students.objects.all())

# 頭5件取得
print(Students.objects.all()[0:5])
print(Students.objects.all()[3:5].query)

# 最初の一件
print(Students.objects.first())

# 絞り込み
print(Students.objects.filter(name="聡志"))
print(Students.objects.filter(age=17))

# AND条件
# grater than(gt) より上
print(Students.objects.filter(name="聡志",id__gt=16))
# less than(lt) 未満
print(Students.objects.filter(name="聡志",id__lt=16))
# grater(less) than equal(gte,lte) 以上,以下
print(Students.objects.filter(name="聡志",id__gte=11,id__lte=16)) 

# 前方一致、後方一致
print(Students.objects.filter(name__startswith="聡").all())
print(Students.objects.filter(name__endswith="志").all())

# or条件
from django.db.models import Q
print(Students.objects.filter(Q(name="聡志") | Q(pk__gt=19)))
