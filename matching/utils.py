from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect, reverse

from user_profile.models import UserProfile
from trip.models import UserTrip
from common import retrieve_none_or_403


def get_current_ut_and_receiver(request, trip_id, receiver_uid):
    current_usertrip = retrieve_none_or_403(request, UserTrip, trip_id)

    try:
        receiver = UserProfile.objects.get(user_id=receiver_uid)
    except ObjectDoesNotExist:
        receiver = None

    if current_usertrip is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    if receiver is None:
        messages.error(request, "Receiver not found")
        return redirect(reverse("trip:view_trips"))

    return current_usertrip, receiver
