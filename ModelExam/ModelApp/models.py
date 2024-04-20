from django.db import models
from django.utils import timezone
import pytz

# Create your models here.

class Tests(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = "tests"
    def __str__(self):
        return f'{self.name}'

class Test_results(models.Model):
    score = models.IntegerField()
    tests = models.ForeignKey(
        "Tests", 
        on_delete=models.CASCADE,
    )
    students = models.ForeignKey(
        "Students", 
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = "test_results"
    def __str__(self):
        return f'{self.tests.name,self.score}'

class Classes(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "classes"
    def __str__(self):
        return f'{self.name}'

class Students(models.Model):
    name = models.CharField(max_length=50)
    grade = models.IntegerField(default=1)
    classes = models.ForeignKey(
        "Classes",
        on_delete=models.CASCADE
    )
    class Meta:
        db_table = "students"
    def __str__(self):
        return f'{self.name,self.grade,self.classes}'
