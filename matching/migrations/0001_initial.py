# Generated by Django 4.1 on 2023-11-20 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("trip", "__first__"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserTripMatches",
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
                    "match_status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Cancelled", "Cancelled"),
                            ("Matched", "Matched"),
                            ("Unmatched", "Unmatched"),
                        ],
                        default="Pending",
                        max_length=10,
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receive_matches",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "receiver_user_trip",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receiver_trip",
                        to="trip.usertrip",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_matches",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender_user_trip",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sender_trip",
                        to="trip.usertrip",
                    ),
                ),
            ],
        ),
    ]
