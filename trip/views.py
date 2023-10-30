from django.shortcuts import render, redirect  # noqa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from . import forms
from .models import Trip


# Create your views here.
@login_required
def create_trip(request):
    if request.method == "POST":
        ut_creation_form = forms.UserTripCreationForm(request.POST)
        if ut_creation_form.is_valid():
            ut_data = ut_creation_form.cleaned_data
            ut_instance = ut_creation_form.save(commit=False)

            trip_instance, _ = Trip.objects.get_or_create(
                destination_city=ut_data["destination_city_ef"],
                destination_country=ut_data["destination_country_ef"],
            )

            ut_instance.trip = trip_instance
            ut_instance.user = request.user
            ut_instance.save()
            messages.success(request, "Successfully created your trip")
            return redirect(reverse("trip:view_trips"))

    ut_creation_form = forms.UserTripCreationForm()
    return render(request, "trip/create_trip.html", {"form": ut_creation_form})


@login_required
def view_trips(request):
    trip_queryset = request.user.usertrip_set.all()
    return render(request, "trip/view_trips.html", {"trips": trip_queryset})
