import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Person

p = Person(
    first_name = "Satoshi",
    last_name="Murakami",
    birthday = "1996-04-03",
    email = "s.m.31043@gmail.com",
    salary = 5000000,
    memo = "memoです",
    web_site = "https://google.com",
)
p = Person(
    first_name = "Satoshi",
    last_name="Murakami",
    birthday = "1996-04-03",
    email = "s.m.31043@gmail.com",
    salary = 5000000,
    memo = "memoです",
    web_site = "",
)
# p.save()

# Person.objects.create(
#     first_name = "minami",
#     last_name="ando",
#     birthday = "1996-04-03",
#     email = "s.m.31043@gmail.com",
#     salary = 5000000,
#     memo = "memoです",
#     web_site = "",
# )


# get_or_create
obj, created = Person.objects.get_or_create(
    first_name = "yusuke",
    last_name="murakami",
    birthday = "1996-04-03",
    email = "s.m.31043@gmail.com",
    salary = 5000000,
    memo = "memoです",
    web_site = "",
)

print(obj)
print(created)
print("実行完了")
