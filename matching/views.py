from functools import reduce

from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date, timedelta
from operator import or_
from django.contrib import messages

from common import retrieve_none_or_403
from trip.models import UserTrip
from .models import UserTripMatches, MatchStatusEnum
from .utils import get_current_ut_and_receiver


@login_required
def show_potential_matches(request, trip_id):
    current_user = request.user
    current_usertrip = retrieve_none_or_403(request, UserTrip, trip_id)

    if current_usertrip is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    # applying dynamic filter to generate match pool
    matching_users = User.objects.filter(
        usertrip__start_trip=current_usertrip.start_trip,
        usertrip__end_trip=current_usertrip.end_trip,
        usertrip__travel_type=current_usertrip.travel_type,
        usertrip__user__userprofile__dob__lt=date.today() - timedelta(days=365.25 * current_user.userprofile.age_lower),
        usertrip__user__userprofile__dob__gt=date.today() - timedelta(days=365.25 * current_user.userprofile.age_upper),
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
    current_matching_users = set(UserTripMatches.objects.filter(
        sender=current_user,
        match_status=MatchStatusEnum.PENDING.value).values_list('receiver', flat=True))
    # Setting the Send Request button off for those users
    matching_users = [
        {
            'user': user,
            'sent_match': True if user.id in current_matching_users else False
        }
        for user in matching_users if user != current_user
    ]

    context = {
        "matching_users": matching_users,
        "trip_id": trip_id,
    }
    return render(request, "matching/list_potential_matches.html", context)


@login_required
def send_matching_request(request, trip_id, receiver_uid):
    current_usertrip, receiver = get_current_ut_and_receiver(request, trip_id, receiver_uid)

    user_trip_matches = UserTripMatches.objects.filter(
        u_trip=current_usertrip,
        sender=request.user,
        match_status=MatchStatusEnum.PENDING.value,
    )
    if any(ut_match.receiver == receiver.user for ut_match in user_trip_matches):
        messages.info(request, "Matching request already sent to user")
    else:
        try:
            user_trip_match = UserTripMatches.objects.get(
                sender=request.user,
                receiver=receiver.user,
                u_trip=current_usertrip,
                match_status=MatchStatusEnum.CANCELLED.value
            )
            user_trip_match.match_status = MatchStatusEnum.PENDING.value
            user_trip_match.save()
            messages.info(request, "Matching request sent to user")
        except UserTripMatches.DoesNotExist:
            new_user_trip_match = UserTripMatches.objects.create(
                sender=request.user,
                receiver=receiver.user,
                u_trip=current_usertrip,
                match_status=MatchStatusEnum.PENDING.value
            )
            new_user_trip_match.save()
            messages.info(request, "Matching request sent to user")

    return redirect(reverse("matching:show_potential_matches", kwargs={'trip_id': trip_id}))


@login_required
def cancel_matching_request(request, trip_id, receiver_uid):
    current_usertrip, receiver = get_current_ut_and_receiver(request, trip_id, receiver_uid)

    try:
        _ = UserTripMatches.objects.get(
            u_trip=current_usertrip,
            sender=request.user,
            receiver=receiver.user,
            match_status=MatchStatusEnum.CANCELLED.value
        )
        messages.info(request, 'Your matching request has already been cancelled.')
    except UserTripMatches.DoesNotExist:
        try:
            user_trip_pending = UserTripMatches.objects.get(
                u_trip=current_usertrip,
                sender=request.user,
                receiver=receiver.user,
                match_status=MatchStatusEnum.PENDING.value
            )
            user_trip_pending.match_status = MatchStatusEnum.CANCELLED.value
            user_trip_pending.save()
            messages.info(request, 'Your matching request is cancelled successfully')
        except Exception as e:
            print(e)
            messages.error(request, f'Your matching request might be accepted, and hence'
                                    f' cannot cancel anymore, please try to unmatch.')
    except UserTripMatches.MultipleObjectsReturned:
        print('This ideally should never happen')
        messages.error(request, f'There are multiple entries for same sender, receiver, u_trip')

    return redirect(reverse("matching:show_potential_matches", kwargs={'trip_id': trip_id}))
