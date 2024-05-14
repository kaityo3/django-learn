# Generated by Django 4.1 on 2024-05-09 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Manufacturers",
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
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField()),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "manufacturers",
            },
        ),
        migrations.CreateModel(
            name="ProductTypes",
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
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField()),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "product_types",
            },
        ),
        migrations.CreateModel(
            name="Products",
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
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField()),
                ("name", models.CharField(max_length=255)),
                ("price", models.IntegerField()),
                ("stock", models.IntegerField()),
                (
                    "manufacturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stores.manufacturers",
                    ),
                ),
                (
                    "product_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="stores.producttypes",
                    ),
                ),
            ],
            options={
                "db_table": "products",
            },
        ),
        migrations.CreateModel(
            name="ProductPictures",
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
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField()),
                ("picture", models.FileField(upload_to="picture")),
                ("order", models.IntegerField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stores.products",
                    ),
                ),
            ],
            options={
                "db_table": "product_pictures",
                "ordering": ["order"],
            },
        ),
    ]
