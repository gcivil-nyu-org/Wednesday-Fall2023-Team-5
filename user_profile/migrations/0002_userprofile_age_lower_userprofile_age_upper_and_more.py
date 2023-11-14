# Generated by Django 4.2.6 on 2023-10-23 02:25

from django.db import migrations, models
import user_profile.models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="age_lower",
            field=models.IntegerField(
                default=0,
                help_text="Enter lower bound for age filter",
                verbose_name="Age(lower bound)",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="age_upper",
            field=models.IntegerField(
                default=99,
                help_text="Enter upper bound for age filter",
                verbose_name="Age(upper bound)",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="drink_pref",
            field=models.CharField(
                choices=[
                    ("Frequently", "Frequently"),
                    ("Socially", "Socially"),
                    ("Rarely", "Rarely"),
                    ("Never", "Never"),
                ],
                default="Never",
                max_length=20,
                verbose_name="Drinking Preferences",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="edu_level",
            field=models.CharField(
                choices=[
                    ("In college", "In college"),
                    ("Undergraduate degree", "Undergraduate degree"),
                    ("In grad school", "In grad school"),
                    ("Graduate degree", "Graduate degree"),
                ],
                default="In college",
                max_length=30,
                verbose_name="Education Level",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="interests",
            field=user_profile.models.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("hiking", "hiking"),
                        ("clubbing", "clubbing"),
                        ("beach", "beach"),
                        ("sightseeing", "sightseeing"),
                        ("bar hopping", "bar hopping"),
                        ("food tourism", "food tourism"),
                        ("museums", "museums"),
                        ("historical/cultural sites", "historical/cultural sites"),
                        ("spa", "spa"),
                        ("relaxed", "relaxed"),
                        ("camping", "camping"),
                        ("sports", "sports"),
                    ],
                    max_length=50,
                ),
                default=list,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="languages",
            field=user_profile.models.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("Chinese", "Chinese"),
                        ("Spanish", "Spanish"),
                        ("English", "English"),
                        ("Arabic", "Arabic"),
                        ("Hindi", "Hindi"),
                        ("Bengali", "Bengali"),
                        ("Portuguese", "Portuguese"),
                        ("Russian", "Russian"),
                        ("Japanese", "Japanese"),
                        ("Urdu", "Urdu"),
                    ],
                    max_length=30,
                ),
                default=list,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="smoke_pref",
            field=models.CharField(
                choices=[
                    ("Socially", "Socially"),
                    ("Regularly", "Regularly"),
                    ("Never", "Never"),
                ],
                default="Never",
                max_length=20,
                verbose_name="Smoking Preferences",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="verified_prof",
            field=models.BooleanField(
                default=False, verbose_name="Verified profiles only?"
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="bio",
            field=models.TextField(
                blank=True, max_length=500, null=True, verbose_name="Bio"
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="dob",
            field=models.DateField(null=True, verbose_name="Date of birth"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="university",
            field=models.TextField(
                max_length=200, null=True, verbose_name="University"
            ),
        ),
    ]