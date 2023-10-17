from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, UserProfile


class AccountRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("dob", "bio", "university")
