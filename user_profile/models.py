# Create your models here.

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    # When you reference the custom user model as a foreign key, use settings.AUTH_USER_MODEL
    # this is because CustomUser has taken the place of User as AUTH_USER_MODEL
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dob = models.DateField(null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    university = models.TextField(max_length=200, null=True)

    def __str__(self):
        return f"User profile for {self.user.username}"
