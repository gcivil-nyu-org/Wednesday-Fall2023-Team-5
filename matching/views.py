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
        trip=current_usertrip.trip,  # destination matching
        user__is_active=True,
        user__userprofile__dob__lte=date.today()
        - timedelta(days=365.25 * current_user.userprofile.age_lower),
        user__userprofile__dob__gt=date.today()
        - timedelta(days=365.25 * current_user.userprofile.age_upper + 1),
    )

    # language filter that filters users with at least one common language
    # apply this filter only if the current user has any language preferences
    if len(current_user.userprofile.languages) != 0:
        # following code combines successive calls to filter() using OR operator avoiding the
        # explicit loop
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
    already_sent_request_users = set(
        UserTripMatches.objects.filter(
            sender=current_user, match_status=MatchStatusEnum.PENDING.value
        ).values_list("receiver", flat=True)
    )

    # excluding users (from matching pool) who have sent a matching request
    # to current user, pending/accepted as a match
    excluding_users = list(
        UserTripMatches.objects.filter(
            receiver=current_user,
            match_status__in=[
                MatchStatusEnum.PENDING.value,
                MatchStatusEnum.MATCHED.value,
            ],
        ).values_list("sender", flat=True)
    )

    # excluding users (from matching pool) who have received a matching request
    # from current user and matched with current user,
    excluding_users += list(
        UserTripMatches.objects.filter(
            sender=current_user,
            match_status=MatchStatusEnum.MATCHED.value,
        ).values_list("receiver", flat=True)
    )

    # Setting the Send Request button off for those users who have already received a request
    # from current user and filtering the excluding users from the match pool

    matching_trips = matching_trips.exclude(user_id__in=excluding_users)

    matching_user_pool = [
        {
            "user": matching_trip.user,
            "sent_match": True
            if matching_trip.user.id in already_sent_request_users
            else False,
            "receiver_utrip_id": matching_trip.id,
        }
        for matching_trip in matching_trips
        if matching_trip.user != current_user
    ]

    # Generate match pool:
    """ Condition-1: If user has not changed the default filters (i.e. all knn attributes are
            blank), use only hard filters Else, use KNN algorithm to generate match pool
            based on ranking
        Condition-2: If the number of potential matches generated using hard filters <
            number of neighbors required to train the KNN, we only use hard filters
            to generate match pool
    """

    current_pool_user_ids = list(matching_trips.values_list("user_id", flat=True))

    if current_user.id not in current_pool_user_ids:
        current_pool_user_ids.append(current_user.id)

    if current_user.id in current_pool_user_ids and len(current_pool_user_ids) >= 3:
        # Prepare data for KNN algorithm:
        current_pool_users = User.objects.filter(id__in=current_pool_user_ids)
        data = pd.DataFrame.from_records(
            current_pool_users.values(
                "userprofile__user",
                "userprofile__drink_pref",
                "userprofile__smoke_pref",
                "userprofile__edu_level",
                "userprofile__interests",
            )
        )
        # get KNN user recommendations (ranked)
        recommendations = get_knn_recommendations(data, current_user.id)
        matching_user_pool = []
        for user_id in recommendations:
            if user_id in current_pool_user_ids and user_id != current_user.id:
                ind_in_pool = current_pool_user_ids.index(user_id)
                matching_trip = matching_trips[ind_in_pool]
                prof_images = list(matching_trip.user.userprofile.userimages_set.all())
                if(len(prof_images) > 0):
                    profile_image = prof_images[0].get_absolute_url()
                    print(profile_image)
                else:
                    profile_image = None
                matching_user_pool.append(
                    {
                        "user": matching_trip.user,
                        "sent_match": True
                        if matching_trip.user.id in already_sent_request_users
                        else False,
                        "receiver_utrip_id": matching_trip.id,
                        "images": profile_image,
                    }
                )

    context = {
        "matching_users": matching_user_pool,
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
    receiver_utrip = UserTrip.objects.get(id=receiver_utrip_id)
    if not receiver_utrip.is_active or not receiver_utrip.user.is_active:
        messages.error(request, "The receiver or their trip is not active anymore.")
        return redirect(
            reverse("matching:show_potential_matches", kwargs={"utrip_id": utrip_id})
        )
    # Cases to be checked before sending request:
    # 1. If the user has already sent a matching request -> just give the info
    # 2. If the receiver has already sent a matching request -> then just inform
    # 3. If there's already any history of sender/receiver, then just update that status
    # 4. If there's no history, then we need to create a fresh one.
    try:
        _ = UserTripMatches.objects.get(
            sender_user_trip_id=utrip_id,
            sender=request.user,
            receiver=receiver.user,
            receiver_user_trip_id=receiver_utrip_id,
            match_status=MatchStatusEnum.PENDING.value,
        )
        messages.info(request, "Matching request already sent to user")
    except UserTripMatches.DoesNotExist:
        try:
            # check if other user has sent any matching request to the current user
            _ = UserTripMatches.objects.get(
                receiver=request.user,
                sender=receiver.user,
                receiver_user_trip_id=utrip_id,
                sender_user_trip_id=receiver_utrip_id,
                match_status=MatchStatusEnum.PENDING.value,
            )
            messages.warning(
                request,
                "The receiver might already have sent a matching "
                "request to you, please check your pending matches",
            )
        except UserTripMatches.DoesNotExist:
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
                "Your matching request might have already been responded, and hence"
                " cannot cancel anymore, "
                "please try to unmatch, if matched or "
                "try sending the request again",
            )
    except UserTripMatches.MultipleObjectsReturned:
        print("This ideally should never happen")
        messages.error(
            request, "There are multiple entries for same sender, receiver, u_trip"
        )

    return redirect(
        reverse("matching:show_potential_matches", kwargs={"utrip_id": utrip_id})
    )


@require_http_methods(["GET"])
@login_required
def show_pending_requests(request, utrip_id):
    usertrip: UserTrip = retrieve_none_or_403(request, UserTrip, utrip_id)

    if usertrip is None:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    if not usertrip.is_active:
        messages.error(
            request, "The trip is not active anymore, cannot show pending request"
        )
        return redirect(reverse("trip:view_trips"))

    pending_matches = UserTripMatches.objects.filter(
        receiver=request.user,
        receiver_user_trip=usertrip,
        sender__is_active=True,
        sender_user_trip__is_active=True,
        match_status=MatchStatusEnum.PENDING.value,
    )
    context = {"pending_matches": pending_matches, "utrip_id": utrip_id}
    return render(request, "matching/list_pending_requests.html", context)


@require_http_methods(["POST"])
@login_required
def react_pending_request(request, utrip_id):
    current_usertrip: UserTrip = retrieve_none_or_403(request, UserTrip, utrip_id)
    sender_utrip_id = request.POST.get("sender_utrip_id")
    sender_id = request.POST.get("sender_id")
    sender_utrip = UserTrip.objects.get(id=sender_utrip_id, user_id=sender_id)
    pending_request: MatchStatusEnum = MatchStatusEnum.get_match_status(
        request.POST.get("pending_request")
    )

    if not current_usertrip.is_active:
        messages.error(
            request,
            "Cannot accept/reject you with other user, as your current trip is inactive.",
        )
        return redirect(reverse("trip:view_trips"))

    if not sender_utrip.is_active or not sender_utrip.user.is_active:
        messages.error(
            request,
            "The sender trip or the sender itself is not active anymore, "
            "cannot accept/reject the request.",
        )
        return redirect(
            reverse("matching:show_pending_requests", kwargs={"utrip_id": utrip_id})
        )

    try:
        # Both current usertrip and the sender's usertrip exists and are active
        # Need to check following conditions:
        # If there is a matching request with the given sender, receiver
        # 1. If the matching request still holds i.e, status is still Pending -> Accept
        # 2. If the matching request is cancelled i.e, status is Cancelled
        #        -> Inform with proper msg
        # 3. If the matching request is Matched/Rejected -> Inform with proper msg
        # 4. If the matching request does not exist, some malfunction,
        #       ideally should not happen
        # 5. If there are more than 1 entry of match available,
        #       could be due to repetition of user, utrip

        matching_request = UserTripMatches.objects.get(
            receiver=request.user,
            sender_id=sender_id,
            receiver_user_trip=current_usertrip,
            sender_user_trip_id=sender_utrip_id,
        )

        if matching_request.match_status == MatchStatusEnum.CANCELLED.value:
            messages.error(
                request,
                "The sender might have cancelled the matching request, "
                "hence could not accept/reject"
                " the current matching request anymore.",
            )
        elif matching_request.match_status == MatchStatusEnum.MATCHED.value:
            messages.info(request, "This matching request has already been accepted")
        elif matching_request.match_status == MatchStatusEnum.REJECTED.value:
            messages.info(request, "This matching request has already been rejected")
        elif matching_request.match_status == MatchStatusEnum.PENDING.value:
            matching_request.match_status = pending_request.value
            matching_request.save()
            if pending_request == MatchStatusEnum.MATCHED:
                messages.info(request, "You are successfully matched with the sender")
                # create new threads if they dont exist
            else:
                messages.info(
                    request, "You have rejected the match request from the sender"
                )

        return redirect(
            reverse("matching:show_pending_requests", kwargs={"utrip_id": utrip_id})
        )
    except UserTrip.DoesNotExist:
        messages.error(
            request,
            "The sender utrip does not exists anymore, sender might"
            "have changed their plans. Sorry you can not accept/reject this request anymore",
        )

    except UserTrip.MultipleObjectsReturned:
        print(
            "Ideally code should not reach here, as user_id, "
            "and utrip_id should be unique for any utrip"
        )
        messages.error(
            request, "There are multiple trips, not sure for which to accept"
        )

    return redirect(
        reverse("matching:show_pending_requests", kwargs={"utrip_id": utrip_id})
    )


@require_http_methods(["GET"])
@login_required
def show_matches(request, utrip_id):
    current_usertrip: UserTrip = retrieve_none_or_403(request, UserTrip, utrip_id)
    if current_usertrip is None or not current_usertrip.is_active:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    matches = UserTripMatches.objects.filter(
        Q(
            sender=request.user,
            sender_user_trip=current_usertrip,
            receiver__is_active=True,
            receiver_user_trip__is_active=True,
            match_status=MatchStatusEnum.MATCHED.value,
        )
        | Q(
            receiver=request.user,
            receiver_user_trip=current_usertrip,
            sender__is_active=True,
            sender_user_trip__is_active=True,
            match_status=MatchStatusEnum.MATCHED.value,
        )
    )
    match_users = [
        match.receiver if match.sender == request.user else match.sender
        for match in matches
    ]
    context = {
        "match_users": match_users,
        "utrip_id": utrip_id,
    }
    return render(request, "matching/list_matches.html", context=context)


@require_http_methods(["POST"])
@login_required
def unmatch(request, utrip_id):
    current_usertrip: UserTrip = retrieve_none_or_403(request, UserTrip, utrip_id)
    other_matched_user_id = request.POST.get("other_uid")

    if current_usertrip is None or not current_usertrip.is_active:
        messages.error(request, "Please select a valid trip")
        return redirect(reverse("trip:view_trips"))

    try:
        matching_utrip = UserTripMatches.objects.get(
            Q(
                sender=request.user,
                receiver_id=other_matched_user_id,
                sender_user_trip=current_usertrip,
                match_status=MatchStatusEnum.MATCHED.value,
            )
            | Q(
                receiver=request.user,
                receiver_user_trip=current_usertrip,
                sender_id=other_matched_user_id,
                match_status=MatchStatusEnum.MATCHED.value,
            )
        )
        matching_utrip.match_status = MatchStatusEnum.UNMATCHED.value
        matching_utrip.save()
    except UserTripMatches.DoesNotExist:
        messages.error(
            request, "No match found, other user might have already unmatched"
        )
    return redirect(reverse("matching:show_matches", kwargs={"utrip_id": utrip_id}))
