# Generated by Django 4.1.5 on 2023-01-28 04:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("business", "0008_alter_shipment_hash"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipment",
            name="destination_country",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="shipment",
            name="expected_price",
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="shipment",
            name="final_price",
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="shipment",
            name="status",
            field=models.CharField(
                choices=[("approved", "approved"), ("not-approved", "not-approved")],
                default="not-approved",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="destination",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="received_shipments",
                to="business.warehouse",
            ),
        ),
    ]
