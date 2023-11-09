from django.shortcuts import render, redirect  # noqa
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from . import forms
from .models import Trip, UserTrip


# Create your views here.
@login_required
def create_trip(request):
    if request.method == "POST":
        usertrip_creation_form = forms.UserTripCreationForm(request.POST)
        if usertrip_creation_form.is_valid():
            usertrip_data = usertrip_creation_form.cleaned_data

            usertrip_instance = usertrip_creation_form.save(commit=False)

            dest_city_raw = usertrip_data["destination_city_ef"]
            dest_city = dest_city_raw[0]

            dest_country_raw = usertrip_data["destination_country_ef"]
            dest_country = dest_country_raw[0]

            trip_instance, _ = Trip.objects.get_or_create(
                destination_city=dest_city,
                destination_country=dest_country,
            )

            usertrip_instance.trip = trip_instance
            usertrip_instance.user = request.user
            usertrip_instance.save()
            messages.success(request, "Successfully created your trip")
            return redirect(reverse("trip:view_trips"))
    else:
        usertrip_creation_form = forms.UserTripCreationForm()

    return render(request, "trip/create_trip.html", {"form": usertrip_creation_form})


@login_required
def view_trips(request):
    trip_queryset = request.user.usertrip_set.all()
    return render(request, "trip/view_trips.html", {"trips": trip_queryset})


@login_required
def detail_trip(request, ut_id):
    # Retrieve trip
    try:
        usertrip_instance = UserTrip.objects.get(id=ut_id)

        if usertrip_instance.user != request.user:
            messages.warning(request, "You're not allowed to view this")
            raise PermissionDenied

    except ObjectDoesNotExist:
        usertrip_instance = None

    if usertrip_instance is not None:
        trip_instance = usertrip_instance.trip

        end_date = usertrip_instance.end_trip

        """
        Filter QS to retrieve associated users
        Filter settings:
        -   Positional argument ~Q used to exclude the user themselves from the
            user set that they see
        Keyword arguments used to:
        -   Make sure that destination combo
            (destination_city, destination_country) are the same (kwarg 1)
        -   Make sure that start_date is greater than the user's specified
            start date (kwarg 2)
        -   Make sure that end_date is greater than the user's specified
            end date (kwarg 3)
        """

        user_qs = User.objects.filter(
            ~Q(id=request.user.id),
            Q(usertrip__trip=trip_instance),
            Q(usertrip__start_trip__lt=end_date),
        )

    else:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    context = {"usertrip_instance": usertrip_instance, "user_qs": user_qs}

    return render(request, "trip/detail_trip.html", context)
