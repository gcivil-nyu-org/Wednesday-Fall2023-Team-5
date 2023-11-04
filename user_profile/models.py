# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from PIL import Image
import os

from common import ChoiceArrayField
from constants import (
    DRINK_PREF_CHOICES,
    SMOKE_PREF_CHOICES,
    EDU_LEVEL_CHOICES,
    INTEREST_CHOICES,
    LANG_CHOICES,
)


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


class UserImages(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="profileImages/",
        blank=True,
    )
    uploaded = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return os.path.join("/media", self.image.name)

    def save(self, *args, **kwargs):
        super().save()
        existing_pic = Image.open(self.image.path)
        output_size = (400, 400)
        existing_pic.thumbnail(output_size)
        existing_pic.save(self.image.path)