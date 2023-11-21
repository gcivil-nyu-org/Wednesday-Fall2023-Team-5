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
from django.contrib.auth.models import User
import datetime

# Import ML libraries:
import pandas as pd
from matching.utilities import get_knn_recommendations


@require_http_methods(["GET"])
@login_required
def show_potential_matches(request, utrip_id):
    current_user = request.user
    current_usertrip: UserTrip = retrieve_none_or_403(request, UserTrip, utrip_id)

    if current_usertrip is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    # applying dynamic filter to generate match pool where
    # usertrip is active AND
    # travel_type = companion AND
    # destination is matching AND
    # trip dates are overlapping (for at least 1 day) AND
    # user is not deactivated AND
    # user's age is in defined range
    matching_trips = UserTrip.objects.filter(
        is_active=True,
        start_trip__lte=current_usertrip.end_trip,
        end_trip__gte=current_usertrip.start_trip,
        travel_type=current_usertrip.travel_type,
        trip=current_usertrip.trip,
        user__is_active=True,
        user__userprofile__dob__lte=date.today()
        - timedelta(days=365.25 * current_user.userprofile.age_lower),
        user__userprofile__dob__gt=date.today()
        - timedelta(days=365.25 * current_user.userprofile.age_upper + 1),
    )

    # language filter that filters users with at least one common language
    # apply this filter only if the current user has any language preferences
    if len(current_user.userprofile.languages) != 0:
        # following code combines successive calls to filter() using OR operator avoiding the explicit loop
        # noinspection PyTypeChecker
        condition = reduce(
            or_,
            [
                Q(user__userprofile__languages__icontains=q)
                for q in current_user.userprofile.languages
            ],
        )
        # additional condition to show matches with at least one common language
        matching_trips = matching_trips.filter(condition)

    # users which have already being sent a matching request by current user, but not yet accepted
    current_matching_users = set(
        UserTripMatches.objects.filter(
            sender=current_user, match_status=MatchStatusEnum.PENDING.value
        ).values_list("receiver", flat=True)
    )

    # users who have sent a matching request to current user, pending/accepted as a match
    matching_users = UserTripMatches.objects.filter(
        receiver=current_user,
        match_status__in=[MatchStatusEnum.PENDING.value, MatchStatusEnum.MATCHED.value],
    ).values_list("sender", flat=True)

    # Setting the Send Request button off for those users who have already received a request
    # from current user
    matching_users = [
        {
            "user": matching_trip.user,
            "sent_match": True
            if matching_trip.user.id in current_matching_users
            else False,
            "receiver_utrip_id": matching_trip.id,
        }
        for matching_trip in matching_trips
        if matching_trip.user != current_user
           and matching_trip.user.id not in matching_users
    ]

    # Generate match pool:
    ''' Condition-1: If user has not changed the default filters (i.e. all knn attributes are blank), use only hard filters
                         Else, use KNN algorithm to generate match pool based on ranking
        Condition-2: If the number of potential matches generated using hard filters < number of neighbors required to 
                    train the KNN, we only use hard filters to generate match pool
    '''
    dynamic_filter_users = list(matching_users.values_list('userprofile__user', flat=True))
    if ((current_user.id in dynamic_filter_users) and (len(dynamic_filter_users) >= 3)):
        # Prepare data for KNN algorithm:
        data = pd.DataFrame.from_records(matching_users.values('userprofile__user', 'userprofile__drink_pref',
                                                               'userprofile__smoke_pref', 'userprofile__edu_level',
                                                               'userprofile__interests'))
        # get KNN user recommendations (ranked)
        recommendations = get_knn_recommendations(data, current_user.id)

        # filter for only knn recommended users
        knn_users = User.objects.filter(id__in=recommendations)

        # filter out the current user from match pool
        knn_users = [user for user in knn_users if user != current_user]

        context = {"matching_users": knn_users,
                   "utrip_id": utrip_id,
                   }
    else:
        # filter out the current user from match pool
        matching_users = [user for user in matching_users if user != current_user]

        context = {"matching_users": matching_users,
                   "utrip_id": utrip_id,
                   }

    return render(request, "matching/list_potential_matches.html", context)


@require_http_methods(["POST"])
@login_required
def send_matching_request(request, utrip_id):
    receiver_uid = request.POST.get("receiver_uid")
    receiver_utrip_id = request.POST.get("receiver_utrip_id")
    current_usertrip, receiver = get_current_ut_and_receiver(
        request, utrip_id, receiver_uid
    )

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
                receiver_user_trip_id=receiver_utrip_id,
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
                match_status=MatchStatusEnum.PENDING.value,
            )
            new_user_trip_match.save()
            messages.info(request, "Matching request sent to user")

    return redirect(
        reverse("matching:show_potential_matches", kwargs={"utrip_id": utrip_id})
    )


@require_http_methods(["POST"])
@login_required
def cancel_matching_request(request, utrip_id):
    receiver_uid = request.POST.get("receiver_uid")
    receiver_utrip_id = request.POST.get("receiver_utrip_id")
    current_usertrip, receiver = get_current_ut_and_receiver(
        request, utrip_id, receiver_uid
    )

    try:
        _ = UserTripMatches.objects.get(
            sender_user_trip_id=utrip_id,
            sender=request.user,
            receiver=receiver.user,
            receiver_user_trip_id=receiver_utrip_id,
            match_status=MatchStatusEnum.CANCELLED.value,
        )
        messages.info(request, "Your matching request has already been cancelled.")
    except UserTripMatches.DoesNotExist:
        try:
            user_trip_pending = UserTripMatches.objects.get(
                sender_user_trip_id=utrip_id,
                sender=request.user,
                receiver=receiver.user,
                receiver_user_trip_id=receiver_utrip_id,
                match_status=MatchStatusEnum.PENDING.value,
            )
            user_trip_pending.match_status = MatchStatusEnum.CANCELLED.value
            user_trip_pending.save()
            messages.info(request, "Your matching request is cancelled successfully")
        except Exception as e:
            print(e)
            messages.error(
                request,
                "Your matching request might be accepted, and hence"
                " cannot cancel anymore, please try to unmatch.",
            )
    except UserTripMatches.MultipleObjectsReturned:
        print("This ideally should never happen")
        messages.error(
            request, "There are multiple entries for same sender, receiver, u_trip"
        )

    return redirect(
        reverse("matching:show_potential_matches", kwargs={"utrip_id": utrip_id})
    )


@login_required
def show_pending_requests(request, utrip_id):
    usertrip = retrieve_none_or_403(request, UserTrip, utrip_id)

    if usertrip is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    pending_matches = UserTripMatches.objects.filter(
        receiver=request.user,
        receiver_user_trip_id=utrip_id,
        match_status=MatchStatusEnum.PENDING.value,
    )
    pending_matches_senders = [pm.sender for pm in pending_matches]
    context = {
        "pending_matching_users": pending_matches_senders,
    }
    return render(request, "matching/list_pending_requests.html", context)
