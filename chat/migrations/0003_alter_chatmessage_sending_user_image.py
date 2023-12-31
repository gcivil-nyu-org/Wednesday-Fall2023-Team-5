# Generated by Django 4.2.7 on 2023-12-10 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0001_initial"),
        ("chat", "0002_chatmessage_sending_user_image_alter_thread_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatmessage",
            name="sending_user_image",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="user_profile.userimages",
            ),
        ),
    ]
