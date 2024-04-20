from django.db import models

# Create your models here.

class Students(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    grade = models.IntegerField()
    picture = models.FileField(upload_to="picture")

    class Meta:
        db_table = 'Student'
