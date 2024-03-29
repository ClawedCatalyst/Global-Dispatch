# Generated by Django 4.1.5 on 2023-01-27 12:00

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="New_User_Resgistration",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255,
                        unique=True,
                        validators=[django.core.validators.EmailValidator()],
                        verbose_name="email address",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OTP",
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
                (
                    "email",
                    models.EmailField(
                        max_length=255,
                        validators=[django.core.validators.EmailValidator()],
                        verbose_name="email address",
                    ),
                ),
                ("otp", models.CharField(blank=True, max_length=4, null=True)),
                ("time", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_verified", models.BooleanField(default=False)),
            ],
        ),
    ]
