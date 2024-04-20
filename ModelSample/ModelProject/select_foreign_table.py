import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Students,Schools,Prefectures,Girl,Boy

# s = Schools.objects.first()
# print(type(s))
# print(dir(s))
# print(s.prefecture.name)
# st = s.students_set
# print(type(st))
# print(dir(st))
# print(s.students_set.all())


# from ModelApp.models import Girl,Boy
# boy1 = Boy.objects.first()
# # print(type(boy1))
# # print(dir(boy1))
# print(boy1.girlfriend.name)

# girl1 = Girl.objects.first()
# # print(type(girl1))
# # print(dir(girl1))
# print(girl1.boy.name)

from ModelApp.models import Books,Authors

b1 = Books.objects.first()
print(b1.authors.all())

a1 = Authors.objects.first()
print(a1.books_set.all())
