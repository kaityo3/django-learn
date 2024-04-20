import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Person

persons = Person.objects.all()
for person in persons:
    # ここで取得するpersonsは、classのMetaで定義した"ordering = ["salary"]"に応じて並ぶ
    print(person.id,person)

# person = Person.objects.get(first_name="Satoshi")
person = Person.objects.get(pk=1)
print(person.id,person)

# filter(絞り込み)
print("*"*80)
persons = Person.objects.filter(first_name="Satoshi")
for person in persons:
    print(person.id,person)
