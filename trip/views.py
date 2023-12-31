from django.shortcuts import render, redirect  # noqa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from . import forms
from .models import Trip, UserTrip
from .helpers import get_emergency_contacts
from common import retrieve_none_or_403


# Create your views here.
@login_required
def create_trip(request):
    if request.method == "POST":
        usertrip_creation_form = forms.UserTripCreationForm(request.POST)
        if usertrip_creation_form.is_valid():
            usertrip_data = usertrip_creation_form.cleaned_data

            dest_city_raw = usertrip_data["destination_city"]
            dest_city = dest_city_raw[0]

            dest_country_raw = usertrip_data["destination_country"]
            dest_country = dest_country_raw[0]

            # 1. Find all active trips of the user.
            # 2. Exclude those trips which are not overlapping with current trip
            overlapping_trips = UserTrip.objects.filter(
                user=request.user, is_active=True
            ).exclude(
                Q(end_trip__lt=usertrip_data["start_trip"])
                | Q(start_trip__gt=usertrip_data["end_trip"])
            )

            if overlapping_trips.exists():
                utrip = overlapping_trips[0]
                message = (
                    f"You have a trip to {utrip.trip.destination_city}, "
                    f"{utrip.trip.destination_country} within the current trip dates,"
                    f" please update that trip or plan for {dest_city}, {dest_country}"
                    f" another time!"
                )
                messages.error(request, message)
                usertrip_creation_form = forms.UserTripCreationForm()
                return render(
                    request, "trip/create_trip.html", {"form": usertrip_creation_form}
                )

            trip_instance, _ = Trip.objects.get_or_create(
                destination_city=dest_city,
                destination_country=dest_country,
            )

            usertrip_instance, created = UserTrip.objects.get_or_create(
                start_trip=usertrip_data["start_trip"],
                end_trip=usertrip_data["end_trip"],
                user=request.user,
                trip=trip_instance,
            )

            if created:
                messages.success(request, "Successfully created your trip")
            else:
                messages.info(
                    request,
                    "You already have an existing trip with same details, "
                    "might wanna update the trip?",
                )
            return redirect(reverse("trip:view_trips"))
    else:
        usertrip_creation_form = forms.UserTripCreationForm()

    return render(request, "trip/create_trip.html", {"form": usertrip_creation_form})


@login_required
def view_trips(request):
    trip_queryset = request.user.usertrip_set.filter(is_active=True)
    return render(request, "trip/view_trips.html", {"trips": trip_queryset})


@login_required
def detail_trip(request, ut_id):
    usertrip_instance: UserTrip = retrieve_none_or_403(
        request, UserTrip, ut_id, "You are not allowed to view this."
    )

    if usertrip_instance is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    emergency_contacts = get_emergency_contacts(
        usertrip_instance.trip.destination_country
    )
    context = {
        "usertrip_instance": usertrip_instance,
        "emergency_contacts": emergency_contacts,
    }

    return render(request, "trip/detail_trip.html", context)


@login_required
def update_trip(request, ut_id):
    usertrip_instance = retrieve_none_or_403(
        request, UserTrip, ut_id, "You are not allowed to edit this."
    )

    if usertrip_instance:
        if request.method == "POST":
            usertrip_update_form = forms.UserTripUpdateForm(
                request.POST, instance=usertrip_instance
            )
            if usertrip_update_form.is_valid():
                usertrip_update_form.save()
                messages.success(request, "Trip successfully edited")
                return redirect(reverse("trip:detail_trip", kwargs={"ut_id": ut_id}))
        else:
            usertrip_update_form = forms.UserTripUpdateForm(instance=usertrip_instance)
    else:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    return render(
        request,
        "trip/update_trip.html",
        {"usertrip_update_form": usertrip_update_form},
    )


@login_required
def milestone_trip(request, ut_id):
    usertrip_instance = retrieve_none_or_403(
        request, UserTrip, ut_id, "You are not allowed to edit this."
    )

    if usertrip_instance and usertrip_instance.is_active:
        if request.method == "POST":
            usertrip_instance.is_active = False
            usertrip_instance.save()
            return redirect(reverse("trip:view_trips"))
    else:
        messages.error(
            request,
            "This trip either does not exist or has been cancelled already.\
            Please select a valid trip",
        )
        return redirect(reverse("trip:view_trips"))

    return render(request, "trip/milestone_confirm.html", {})
