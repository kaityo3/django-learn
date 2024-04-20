import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Boy,Girl

boylist = ["Aくん","Bくん"]
girllist = ["Xちゃん","Yちゃん"]

Girl.objects.all().delete()
# Boy.objects.all().delete()


for i,girl in enumerate(girllist):
	girl_c = Girl(name = girl)
	girl_c.save()
	Boy.objects.create(
        name = boylist[i],
        girlfriend = girl_c
    )
