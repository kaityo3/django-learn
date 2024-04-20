import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Students,Person

# IN
ids = [1,13,20]
print(Students.objects.filter(pk__in=ids).all())

# contain-部分一致
print(Students.objects.filter(name__contains="介"))

# isnull
print(Person.objects.filter(salary__isnull=True))

# レコードを取り除く(filter → exclude)
print(Person.objects.exclude(salary__isnull=True))
print(Students.objects.exclude(name__contains="介"))

# 一部のカラムを取り除く
print(Students.objects.values("name","age").query)
students = Students.objects.values("name","age")
for  student in students:
    print(student["name"])

# 並び替え
print(Students.objects.order_by("name","-id"))
