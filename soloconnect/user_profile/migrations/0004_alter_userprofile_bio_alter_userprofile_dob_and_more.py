# Generated by Django 4.2.6 on 2023-10-10 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_profile", "0003_userprofile_alter_customuser_managers_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="bio",
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile", name="dob", field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="university",
            field=models.TextField(max_length=100, null=True),
        ),
    ]
