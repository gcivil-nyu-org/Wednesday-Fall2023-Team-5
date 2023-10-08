from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# not fully finished yet
class CustomUser(AbstractUser):
    ## for user interaction
    username = None
    dob = models.DateField()
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = email

    def __str__(self):
        return f"fname: {self.first_name}, lname: {self.last_name}, email: {self.email}"
