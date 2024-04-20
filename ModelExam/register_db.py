import os
import random

# 環境変数定義
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelExam.settings")
from django import setup
setup()

from ModelApp.models import Tests,Test_results,Students,Classes

subjects = ["数学","英語","国語"]
classes_name = [f"class{chr(i)}" for i in range(ord('A'),ord('J')+1) ]
students_name = [f"students{chr(i)}" for i in range(ord('A'),ord('J')+1)]

def insert_tests():
    for subject in subjects:
        Tests.objects.create(
            name = subject 
        )

def insert_classes():
    for class_name in classes_name:
        class_cls = Classes(
            name = class_name
        )
        class_cls.save()

        for student_name in students_name:
            student = Students(
                name = student_name,
                classes = class_cls,
                grade = 1,
            )
            student.save()
            
            for tests in Tests.objects.all():
                test_result = Test_results(
                    tests = tests,
                    students = student,
                    score = random.randint(50,100),
                )
                test_result.save()

# insert_tests()
# insert_classes()
                

st1 = Students.objects.first()
# print(type(st1.test_results_set.all().first()))
# print(dir(st1.test_results_set.all().first()))

# idが1のstudentsの名前とテストの科目と点数を表示する。
print(st1.id,st1.name,st1.classes.name)
for subject in st1.test_results_set.all():
    print(subject.tests.name,subject.score)

#クラス毎の各科目のテストの合計、平均、最大、最小を表示する。
from django.db.models import Count,Max,Min,Avg,Sum


for class_cls in (Classes.objects.values("name","students__test_results__tests__name").annotate(
    avg = Avg("students__test_results__score"),
    max = Max("students__test_results__score"),
    min = Min("students__test_results__score")
    )):
    print(class_cls["name"],
          class_cls["students__test_results__tests__name"],
          class_cls["avg"],class_cls["max"],class_cls["min"]
          )


            
        

    

    
