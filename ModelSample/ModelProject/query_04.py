import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Students,Schools

# 外部テーブルでフィルター
for student in Students.objects.filter(school__name="南高校").all():
    print(student.name,student.school.name,student.school.prefecture.name)

# 外部テーブルでexclude
for student in Students.objects.exclude(school__name="南高校").all():
    print(student.name,student.school.name,student.school.prefecture.name)

# 外部テーブルでフィルター(参照先からも可能)
print(Schools.objects.filter(students__name="聡志"))

print("-"*100)
# 外部テーブルでorder_by
for student in Students.objects.order_by("-school__name").all():
    print(student.name,student.school.name)

# 外部テーブルでGroupBy
from django.db.models import Count,Max
print(Students.objects.values("school__name").annotate(Count("id"),Max("id")))
