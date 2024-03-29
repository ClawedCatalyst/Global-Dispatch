# Generated by Django 4.1.5 on 2023-01-27 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Business",
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
                ("name", models.CharField(max_length=255)),
                ("owner_name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="WareHouse",
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
                ("max_capacity", models.PositiveBigIntegerField()),
                ("present_capacity", models.PositiveBigIntegerField(default=0)),
                ("location", models.CharField(max_length=255)),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="business.business",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Commodity",
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
                ("name", models.CharField(max_length=255)),
                (
                    "warehouse",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="business.warehouse",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=255)),
                ("quantity", models.PositiveBigIntegerField()),
                ("volume", models.PositiveBigIntegerField()),
                (
                    "commodity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="business.commodity",
                    ),
                ),
            ],
        ),
    ]
