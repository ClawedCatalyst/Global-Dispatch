# Generated by Django 4.1.5 on 2023-01-27 20:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("business", "0007_shipment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shipment",
            name="hash",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
