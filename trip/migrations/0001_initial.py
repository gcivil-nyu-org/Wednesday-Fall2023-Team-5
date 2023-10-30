# Generated by Django 4.2.6 on 2023-10-29 17:55

import common
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Trip",
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
                ("destination_city", models.CharField(max_length=500)),
                ("destination_country", models.CharField(max_length=500)),
                ("start_trip", models.DateTimeField(verbose_name="start_trip")),
                ("end_trip", models.DateTimeField(verbose_name="end_trip")),
                (
                    "travel_type",
                    common.ChoiceArrayField(
                        base_field=models.CharField(
                            choices=[("Solo", "Solo"), ("Companion", "Companion")],
                            max_length=30,
                        ),
                        default=list,
                        size=None,
                    ),
                ),
            ],
        ),
    ]