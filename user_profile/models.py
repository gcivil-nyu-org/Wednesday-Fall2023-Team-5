# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django import forms

DRINK_PREF_CHOICES = [
    ("Frequently", "Frequently"),
    ("Socially", "Socially"),
    ("Rarely", "Rarely"),
    ("Never", "Never"),
]

SMOKE_PREF_CHOICES = [
    ("Socially", "Socially"),
    ("Regularly", "Regularly"),
    ("Never", "Never"),
]

EDU_LEVEL_CHOICES = [
    ("In college", "In college"),
    ("Undergraduate degree", "Undergraduate degree"),
    ("In grad school", "In grad school"),
    ("Graduate degree", "Graduate degree"),
]

INTEREST_CHOICES = [
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
]

LANG_CHOICES = [
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
]


# ------- Creating new class of array field using postgres.fields -------
class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.

    Usage:

        choices = ChoiceArrayField(models.CharField(max_length=...,
                                                    choices=(...,)),
                                   default=[...])
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": forms.CheckboxSelectMultiple,  # remove this for list selection
        }
        defaults.update(kwargs)

        return super(ArrayField, self).formfield(**defaults)


# ----------------------------------------------------------------------


class UserProfile(models.Model):
    # When you reference the custom user model as a foreign key, use settings.AUTH_USER_MODEL
    # this is because CustomUser has taken the place of User as AUTH_USER_MODEL
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dob = models.DateField(null=True, verbose_name="Date of birth")
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="Bio")
    university = models.TextField(max_length=200, null=True, verbose_name="University")

    # Matching preference filters
    age_lower = models.IntegerField(
        default=0,
        verbose_name="Age(lower bound)",
        help_text="Enter lower bound for age filter",
    )
    age_upper = models.IntegerField(
        default=99,
        verbose_name="Age(upper bound)",
        help_text="Enter upper bound for age filter",
    )
    verified_prof = models.BooleanField(
        default=False, verbose_name="Verified profiles only?"
    )
    drink_pref = models.CharField(
        max_length=20,
        choices=DRINK_PREF_CHOICES,
        verbose_name="Drinking Preferences",
        default="Never",
    )
    smoke_pref = models.CharField(
        max_length=20,
        choices=SMOKE_PREF_CHOICES,
        verbose_name="Smoking Preferences",
        default="Never",
    )
    edu_level = models.CharField(
        max_length=30,
        choices=EDU_LEVEL_CHOICES,
        verbose_name="Education Level",
        default="In college",
    )
    # Using postgres ArrayField
    interests = ChoiceArrayField(
        models.CharField(max_length=50, choices=INTEREST_CHOICES), default=list
    )
    languages = ChoiceArrayField(
        models.CharField(max_length=30, choices=LANG_CHOICES), default=list
    )

    def __str__(self):
        return f"User profile for {self.user.username}"
