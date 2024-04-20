import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Person

# Person.objects.filter(first_name = "satoshi").delete()

# Person.objects.filter(first_name = "None",last_name="Murakami")

Person.objects.all().delete()
