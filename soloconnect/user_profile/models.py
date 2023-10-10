from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from .helpers import PREFERENCE_MAP


class UserManager(BaseUserManager):
    use_in_migrations = True

    """
    This user manager class needs to be defined so we can use emails as usernames.
    
    Think of _create_user() as the overall user creation function- user and superuser are both User
    so while create_user and create_superuser will perform the necessary validations for
    each "subclass" of User, they will each then pass the appropriate arguments into _create_user()
    and that function will take care of actually creating the user.
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is False:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is False:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"fname: {self.first_name}, lname: {self.last_name}, email: {self.email}"


class UserProfile(models.Model):
    # When you reference the custom user model as a foreign key, use settings.AUTH_USER_MODEL
    # this is because CustomUser has taken the place of User as AUTH_USER_MODEL
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    dob = models.DateField(null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    university = models.TextField(max_length=200, null=True)

    # profile_picture = models.ImageField()
    # matching = ArrayField() mapped to PREFERENCE_MAP (from helpers.py)
    def __str__(self):
        return f"User profile for {self.user.email}"
