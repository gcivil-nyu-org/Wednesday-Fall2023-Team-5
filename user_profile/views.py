# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import logging

from . import forms


# Create your views here.


# User Profile CRUD
def create_user_account(request):
    logger = logging.getLogger("django")
    if request.method == "POST":
        registration_form = forms.AccountRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            logger.info("Saved form")
            return redirect(reverse("user_profile:login"))
    else:
        registration_form = forms.AccountRegistrationForm()

    return render(
        request, "user_profile/user_registration.html", {"acc_form": registration_form}
    )


@login_required
def view_profile(request):
    bio = "There's nothing here"
    university = "There's nothing here"
    logger = logging.getLogger("django")
    logger.info("Here in view profile")
    if request.user.userprofile.bio is not None:
        bio = request.user.userprofile.bio
    if request.user.userprofile.university is not None:
        university = request.user.userprofile.university

    context = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "bio": bio,
        "university": university,
    }
    return render(request, "user_profile/view_profile.html", context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        profile_form = forms.ProfileUpdateForm(
            request.POST, instance=request.user.userprofile
        )
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse("user_profile:view_profile"))

    profile_form = forms.ProfileUpdateForm(instance=request.user.userprofile)

    return render(
        request, "user_profile/edit_profile.html", {"profile_form": profile_form}
    )


@login_required
def milestone_profile(request):
    if request.method == "POST":
        try:
            current_user = User.objects.get(pk=request.user.pk)
        except ObjectDoesNotExist:
            messages.error(
                request, "Encountered a user does not exist error- please try again"
            )
        else:
            current_user.is_active = False
            current_user.save()
            return redirect(reverse("home_default:home_page"))

    return render(request, "user_profile/milestone_confirm.html", {})


# Login/logout views
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user_instance = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user_instance = None

        if user_instance is not None:
            if not user_instance.is_active:
                user_instance.is_active = True
                user_instance.save()
                messages.success(request, "Successfully reactivated account")

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect(reverse("user_profile:view_profile"))
        else:
            messages.info(request, "Please enter a valid username and password")

    auth_form = AuthenticationForm()
    return render(request, "user_profile/login.html", {"form": auth_form})
