from functools import reduce

from django.db.models import ExpressionWrapper, IntegerField, F, Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from trip.models import UserTrip
import datetime
from datetime import date
from operator import or_


@login_required
def show_potential_matches(request, trip_id):
    current_user = request.user
    current_usertrip = UserTrip.objects.get(id=trip_id)
    # all_user_profiles = UserTrip.objects.all()

    matching_users = User.objects.filter(
        usertrip__start_trip=current_usertrip.start_trip,
        usertrip__end_trip=current_usertrip.end_trip,
        usertrip__travel_type=current_usertrip.travel_type,
        usertrip__user__userprofile__dob__lt=date.today()
        - datetime.timedelta(days=365.25 * current_user.userprofile.age_lower),
        usertrip__user__userprofile__dob__gt=date.today()
        - datetime.timedelta(days=365.25 * current_user.userprofile.age_upper),
        usertrip__user__userprofile__verified_prof=current_user.userprofile.verified_prof,
        # without last filter - {changing chinese, spanish}, User3, User6, User7 must be there
        usertrip__trip__destination_city=current_usertrip.trip.destination_city,
        usertrip__trip__destination_country=current_usertrip.trip.destination_country,
    ).distinct()

    condition = reduce(
        or_,
        [
            Q(usertrip__user__userprofile__languages__icontains=q)
            for q in current_user.userprofile.languages
        ],
    )
    matching_users = matching_users.filter(condition)

    context = {"matching_users": matching_users, "current_user": current_user}
    return render(request, "matching/list_potential_matches.html", context)
