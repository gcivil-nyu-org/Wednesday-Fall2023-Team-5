from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.forms import inlineformset_factory
from .models import UserImages, UserProfile
from .forms import ImageUploadForm
import logging

from . import forms


# User Profile CRUD
def create_user_account(request):
    logger = logging.getLogger("django")
    if request.method == "POST":
        registration_form = forms.AccountRegistrationForm(request.POST)
        if registration_form.is_valid():
            # Save the registration form
            registration_form.save()
            # Retrieve cleaned data from registration form
            reg_form_data = registration_form.cleaned_data
            logger.info("Saved form")
            # Authenticate and log in user
            user_auth = authenticate(username=reg_form_data["username"], password=reg_form_data["password1"])
            login(request, user_auth)
            messages.success(
                request, "Successfully created your account and logged you in. Please create your profile."
            )
            return redirect(reverse("user_profile:edit_profile"))
    else:
        registration_form = forms.AccountRegistrationForm()

    return render(
        request, "user_profile/user_registration.html", {"acc_form": registration_form}
    )


def detail_profile(request, id):
    # fetch the target user according to id parameter passed
    # through url or throw a 404
    try:
        target_user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        target_user = None

    if target_user is not None:
        if target_user.is_active:
            image_qs = target_user.userprofile.userimages_set.all()

            if image_qs:
                qs_range = range(1, len(image_qs))
            else:
                qs_range = None

            context = {
                "first_name": target_user.first_name,
                "last_name": target_user.last_name,
                "bio": target_user.userprofile.bio,
                "university": target_user.userprofile.university,
                "verified_prof": target_user.userprofile.verified_prof,
                "drink_pref": target_user.userprofile.drink_pref,
                "smoke_pref": target_user.userprofile.smoke_pref,
                "edu_level": target_user.userprofile.edu_level,
                "interests": target_user.userprofile.interests,
                "languages": target_user.userprofile.languages,
                "images": image_qs,
                "qs_range": qs_range,
            }
            return render(request, "user_profile/detail_profile.html", context)
        else:
            return render(request, "user_profile/detail_profile_inactive.html", {})

    messages.error(request, "The requested user profile was not found")
    return redirect(reverse("home_default:home_page"))


@login_required
def view_profile(request):
    logger = logging.getLogger("django")
    logger.info("Here in view profile")

    image_qs = request.user.userprofile.userimages_set.all()

    if image_qs:
        qs_range = range(1, len(image_qs))
    else:
        qs_range = None

    context = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "bio": request.user.userprofile.bio,
        "university": request.user.userprofile.university,
        "age_lower": request.user.userprofile.age_lower,
        "age_upper": request.user.userprofile.age_upper,
        "verified_prof": request.user.userprofile.verified_prof,
        "drink_pref": request.user.userprofile.drink_pref,
        "smoke_pref": request.user.userprofile.smoke_pref,
        "edu_level": request.user.userprofile.edu_level,
        "interests": request.user.userprofile.interests,
        "languages": request.user.userprofile.languages,
        "images": image_qs,
        "qs_range": qs_range,
    }

    return render(request, "user_profile/view_profile.html", context)


@login_required
def edit_profile(request):
    user_profile_instance = request.user.userprofile

    if request.method == "POST":
        profile_form = forms.ProfileUpdateForm(
            request.POST, instance=user_profile_instance
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile successfully edited")
            return redirect(reverse("user_profile:view_profile"))
    else:
        profile_form = forms.ProfileUpdateForm(instance=user_profile_instance)

    return render(
        request,
        "user_profile/edit_profile.html",
        {"profile_form": profile_form},
    )


@login_required
def upload_images(request):
    user_profile_instance = request.user.userprofile

    ImageFormSet = inlineformset_factory(
        UserProfile,
        UserImages,
        ImageUploadForm,
        can_delete=False,
        max_num=5,
        extra=5,
    )

    if request.method == "POST":
        image_formset = ImageFormSet(
            request.POST, request.FILES, instance=user_profile_instance
        )
        if image_formset.is_valid():
            image_formset.save()
            messages.success(request, "Photos successfully uploaded")
            return redirect(reverse("user_profile:view_profile"))
        else:
            messages.error(request, "Unable to upload photos; please try again")

    image_formset = ImageFormSet(instance=user_profile_instance)

    return render(
        request, "user_profile/upload_images.html", {"image_formset": image_formset}
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
            user = User.objects.get(username=username)

            if not user.check_password(password):
                raise Exception("Incorrect Password")

            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, "Successfully reactivated account")

            user = authenticate(request, username=username, password=password)
        except Exception as e:
            print(e)
            user = None

        if user is None:
            messages.error(request, "Please enter a valid username and password")
        else:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect(reverse("user_profile:view_profile"))

    auth_form = AuthenticationForm()
    return render(request, "user_profile/login.html", {"form": auth_form})
