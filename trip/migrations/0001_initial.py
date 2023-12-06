# Generated by Django 4.1 on 2023-11-20 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

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
                (
                    "destination_city",
                    models.CharField(max_length=500, verbose_name="Destination City"),
                ),
                (
                    "destination_country",
                    models.CharField(
                        max_length=500, verbose_name="Destination Country"
                    ),
                ),
            ],
            options={
                "unique_together": {("destination_country", "destination_city")},
            },
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
                (
                    "start_trip",
                    models.DateField(
                        help_text="Enter the date you will arrive at your destination",
                        verbose_name="Trip Start Date",
                    ),
                ),
                (
                    "end_trip",
                    models.DateField(
                        help_text="Enter the date you plan to leave your destination",
                        verbose_name="Trip End Date",
                    ),
                ),
                (
                    "travel_type",
                    models.CharField(
                        choices=[("Solo", "Solo"), ("Companion", "Companion")],
                        max_length=30,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
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
