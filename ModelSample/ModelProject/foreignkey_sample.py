import os

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup
setup()

from ModelApp.models import Students,Schools,Prefectures

prefectures = ["東京","名古屋","大阪","三重"]
schools = ["東高校","西高校","北高校","南高校"]
students = ["聡志","南美","悠介"]


def insert_records():
    Prefectures.objects.all().delete()
    Students.objects.all().delete()
    Schools.objects.all().delete()

    for perfecture_name in prefectures:
        prefecture = Prefectures(
            name = perfecture_name
        )
        prefecture.save()

        for school_name in schools:
            school = Schools(
                name = school_name,
                prefecture = prefecture
            )
            school.save()
            
            for student_name in students:
                student = Students(
                    name = student_name,
                    age=17,
                    major="物理",
                    school = school,
                    prefecture = prefecture
                )
                student.save()

def select_students():
    students = Students.objects.all()
    for student in students:
        print(
            student.id,
            student.name,
            student.school.id,
            student.school.name,
            student.school.prefecture.id,
            student.school.prefecture.name
        )


insert_records()
# select_students()

# 以下、Schoolクラスのid=1(1.東高校-東京)に該当するレコードが削除される。
# Studentクラスで"Schoolクラスのid=1(1.東高校-東京)"を参照していたレコードも同時に削除される(CASCADE指定によるもの)
# Schools.objects.filter(id=1).delete()

# 以下Prefecturesクラスのid=1(1.東京)に該当するレコードが削除される。
# それに伴い、School,Studentクラスで、東京を参照していたレコードも同時に削除される(CASCADE)
# Prefectures.objects.filter(id=1).delete()
