from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .helpers import email_is_valid
from .models import User, UserProfile


# CRUD Forms
class AccountRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")

        if not email_is_valid(email):
            raise ValidationError("Email must end in .edu")

        return cleaned_data

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("dob", "bio", "university")
