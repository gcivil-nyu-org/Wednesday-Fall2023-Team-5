# Generated by Django 4.2.7 on 2023-12-11 03:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0005_chatmessage_receiving_image_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatmessage",
            name="receiving_image_url",
        ),
        migrations.RemoveField(
            model_name="chatmessage",
            name="sending_image_url",
        ),
        migrations.AddField(
            model_name="thread",
            name="first_user_image_url",
            field=models.CharField(default=""),
        ),
        migrations.AddField(
            model_name="thread",
            name="second_user_image_url",
            field=models.CharField(default=""),
        ),
    ]
