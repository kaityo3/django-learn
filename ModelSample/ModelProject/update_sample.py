import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Person
from django.utils import timezone
import pytz

person = Person.objects.get(id=1)
print(person)
person.birthday = "2001-01-01"
person.update_at = timezone.datetime.now(pytz.timezone("Asia/Tokyo"))
person.salary = 1000000
person.save()

peaple = Person.objects.filter(first_name = "Satoshi")
for person in peaple:
    person.first_name = person.first_name.lower()
    person.update_at = timezone.datetime.now(pytz.timezone("Asia/Tokyo"))
    person.save()

# クエリとして一括で修正できるため実行速度が速い
Person.objects.filter(first_name = "satoshi").update(
    salary = 10000000,
    update_at = timezone.datetime.now(pytz.timezone("Asia/Tokyo"))
)
