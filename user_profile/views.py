# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
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
        currentUser = User.objects.get(pk=request.user.pk)
        currentUser.is_active = False
        currentUser.save()
        return redirect(reverse("home_default:home_page"))
    return render(request, "user_profile/milestone_confirm.html", {})
