from functools import reduce

from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from trip.models import UserTrip
import datetime
from datetime import date
from operator import or_
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib import messages


@login_required
def show_potential_matches(request, trip_id):
    current_user = request.user
    try:
        current_usertrip = UserTrip.objects.get(id=trip_id)
    except ObjectDoesNotExist:
        current_usertrip = None

    if current_usertrip is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    if current_usertrip.user.id != current_user.id:
        messages.warning(request, "You're not allowed to view this")
        raise PermissionDenied

    # applying dynamic filter to generate match pool
    matching_users = User.objects.filter(
        usertrip__start_trip=current_usertrip.start_trip,
        usertrip__end_trip=current_usertrip.end_trip,
        usertrip__travel_type=current_usertrip.travel_type,
        usertrip__user__userprofile__dob__lt=date.today()
        - datetime.timedelta(days=365.25 * current_user.userprofile.age_lower),
        usertrip__user__userprofile__dob__gt=date.today()
        - datetime.timedelta(days=365.25 * current_user.userprofile.age_upper),
        usertrip__user__userprofile__verified_prof=current_user.userprofile.verified_prof,
        usertrip__trip__destination_city=current_usertrip.trip.destination_city,
        usertrip__trip__destination_country=current_usertrip.trip.destination_country,
    ).distinct()

    try:
        condition = reduce(
            or_,
            [
                Q(usertrip__user__userprofile__languages__icontains=q)
                for q in current_user.userprofile.languages
            ],
        )
        # additional condition to show matches with at least one common language
        matching_users = matching_users.filter(condition)
    except Exception as e:
        print(e)

    # filter out the current user from match pool
    matching_users = [user for user in matching_users if user != current_user]

    context = {"matching_users": matching_users}
    return render(request, "matching/list_potential_matches.html", context)
