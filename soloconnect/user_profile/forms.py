from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, UserProfile


class AccountRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email")

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("dob", "bio", "university")

