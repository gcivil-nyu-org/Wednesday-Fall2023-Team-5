from django.shortcuts import render, redirect
from django.urls import reverse
from .models import CustomUser, UserProfile
from django.conf import settings
from . import forms

# Create your views here.

# User Profile CRUD
def create_user_account(request):
    if request.method == "POST":
        registration_form = forms.AccountRegistrationForm(request.POST)
        profile_form = forms.ProfileCreationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect(reverse('login'))
    else:
        registration_form = forms.AccountRegistrationForm()

    return render(request, 'user_profile/user_registration.html', {"acc_form": registration_form})

