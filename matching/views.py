from functools import reduce

from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import date, timedelta
from operator import or_
from django.contrib import messages

from common import retrieve_none_or_403
from trip.models import UserTrip
from .models import UserTripMatches, MatchStatusEnum
from .utils import get_current_ut_and_receiver


@require_http_methods(['GET'])
@login_required
def show_potential_matches(request, utrip_id):
    current_user = request.user
    current_usertrip: UserTrip = retrieve_none_or_403(request, UserTrip, utrip_id)

    if current_usertrip is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    # applying dynamic filter to generate match pool
    matching_trips = UserTrip.objects.filter(
        start_trip=current_usertrip.start_trip,
        end_trip=current_usertrip.end_trip,
        travel_type=current_usertrip.travel_type,
        trip__destination_city=current_usertrip.trip.destination_city,
        trip__destination_country=current_usertrip.trip.destination_country,
        user__userprofile__dob__lt=date.today() - timedelta(days=365.25 * current_user.userprofile.age_lower),
        user__userprofile__dob__gt=date.today() - timedelta(days=365.25 * current_user.userprofile.age_upper)
    )

    try:
        condition = reduce(
            or_,
            [
                Q(user__userprofile__languages__icontains=q)
                for q in current_user.userprofile.languages
            ],
        )
        # additional condition to show matches with at least one common language
        matching_trips = matching_trips.filter(condition)
    except Exception as e:
        print(e)

    # filter out the current user from match pool
    current_matching_users = set(UserTripMatches.objects.filter(
        sender=current_user,
        match_status=MatchStatusEnum.PENDING.value).values_list('receiver', flat=True))

    # Setting the Send Request button off for those users
    matching_users = [
        {
            'user': matching_trip.user,
            'sent_match': True if matching_trip.user.id in current_matching_users else False,
            'receiver_utrip_id': matching_trip.id,
        }
        for matching_trip in matching_trips if matching_trip.user != current_user
    ]

    context = {
        "matching_users": matching_users,
        "utrip_id": utrip_id,
    }
    return render(request, "matching/list_potential_matches.html", context)


@require_http_methods(['POST'])
@login_required
def send_matching_request(request, utrip_id):
    receiver_uid = request.POST.get('receiver_uid')
    receiver_utrip_id = request.POST.get('receiver_utrip_id')
    current_usertrip, receiver = get_current_ut_and_receiver(request, utrip_id, receiver_uid)

    try:
        _ = UserTripMatches.objects.get(
            sender_user_trip_id=utrip_id,
            sender=request.user,
            receiver=receiver.user,
            receiver_user_trip_id=receiver_utrip_id,
            match_status=MatchStatusEnum.PENDING.value,
        )
        messages.info(request, "Matching request already sent to user")
    except Exception as e:
        print(e)
        try:
            user_trip_match = UserTripMatches.objects.get(
                sender=request.user,
                receiver=receiver.user,
                sender_user_trip_id=utrip_id,
                receiver_user_trip_id=receiver_utrip_id
            )
            user_trip_match.match_status = MatchStatusEnum.PENDING.value
            user_trip_match.save()
            messages.info(request, "Matching request sent to user")
        except UserTripMatches.DoesNotExist:
            receiver_user_trip = UserTrip.objects.get(id=receiver_utrip_id)
            new_user_trip_match = UserTripMatches.objects.create(
                sender=request.user,
                receiver=receiver.user,
                sender_user_trip=current_usertrip,
                receiver_user_trip=receiver_user_trip,
                match_status=MatchStatusEnum.PENDING.value
            )
            new_user_trip_match.save()
            messages.info(request, "Matching request sent to user")

    return redirect(reverse("matching:show_potential_matches", kwargs={'utrip_id': utrip_id}))


@require_http_methods(['POST'])
@login_required
def cancel_matching_request(request, utrip_id):
    receiver_uid = request.POST.get('receiver_uid')
    receiver_utrip_id = request.POST.get('receiver_utrip_id')
    current_usertrip, receiver = get_current_ut_and_receiver(request, utrip_id, receiver_uid)

    try:
        _ = UserTripMatches.objects.get(
            sender_user_trip_id=utrip_id,
            sender=request.user,
            receiver=receiver.user,
            receiver_user_trip_id=receiver_utrip_id,
            match_status=MatchStatusEnum.CANCELLED.value
        )
        messages.info(request, 'Your matching request has already been cancelled.')
    except UserTripMatches.DoesNotExist:
        try:
            user_trip_pending = UserTripMatches.objects.get(
                sender_user_trip_id=utrip_id,
                sender=request.user,
                receiver=receiver.user,
                receiver_user_trip_id=receiver_utrip_id,
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

    return redirect(reverse("matching:show_potential_matches", kwargs={'utrip_id': utrip_id}))


@login_required
def show_pending_requests(request, utrip_id):
    usertrip = retrieve_none_or_403(request, UserTrip, utrip_id)

    if usertrip is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    pending_matches = UserTripMatches.objects.filter(
        receiver=request.user,
        match_status=MatchStatusEnum.PENDING.value
    )
    print(f'{pending_matches = }')
    pending_matches_senders = [pm.sender for pm in pending_matches]
    return render(request, "matching/list_pending_requests.html",
                  {'pending_senders': pending_matches_senders})
