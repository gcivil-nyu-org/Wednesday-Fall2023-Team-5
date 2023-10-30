# Generated by Django 4.2.6 on 2023-10-30 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("trip", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trip",
            name="end_trip",
        ),
        migrations.RemoveField(
            model_name="trip",
            name="start_trip",
        ),
        migrations.CreateModel(
            name="UserTrip",
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
                ("start_trip", models.DateTimeField(verbose_name="start_trip")),
                ("end_trip", models.DateTimeField(verbose_name="end_trip")),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="trip.trip"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
