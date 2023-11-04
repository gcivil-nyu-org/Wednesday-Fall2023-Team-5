from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .helpers import email_is_valid
from .models import User, UserProfile, UserImages


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
        fields = (
            "dob",
            "bio",
            "university",
            "age_lower",
            "age_upper",
            "verified_prof",
            "drink_pref",
            "smoke_pref",
            "edu_level",
            "interests",
            "languages",
        )
        labels = {
            "interests": "Interests",
            "languages": "Languages",
        }


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImages
        fields = ["image"]
        labels = {"image": "Upload Image"}
