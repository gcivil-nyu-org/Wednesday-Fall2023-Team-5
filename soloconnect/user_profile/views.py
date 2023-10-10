from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from . import forms

# Create your views here.

# User Profile CRUD
def create_user_account(request):
    if request.method == "POST":
        registration_form = forms.AccountRegistrationForm(request.POST)
        profile_form = forms.ProfileCreationForm(request.POST)
        if registration_form.is_valid() and profile_form.is_valid():
            registration_form.save()
            profile_form.save()
            # THIS HAS NOT BEEN CREATED - IT WILL 404 IF UNCOMMENTED
            # redirect(reverse('add_matching_preferences'))
            return redirect(reverse('home_page'))
    else:
        registration_form = forms.AccountRegistrationForm()
        profile_form = forms.ProfileCreationForm()

    return render(request, 'user_profile/user_registration.html', {"acc_form": registration_form, "prof_form": profile_form})

