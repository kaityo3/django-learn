# Generated by Django 4.1 on 2024-04-17 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FormApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelSetPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("memo", models.CharField(max_length=255)),
            ],
        ),
    ]
