import json
import logging

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from common import db_retrieve_or_none
from matching.models import UserTripMatches
from .models import Thread
from django.db.models import Q


@login_required
def threads_page(request):
    print(" Here in threads")
    threads = (
        Thread.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
        .prefetch_related("chat_message")
        .order_by("timestamp")
    )
    # if not threads:
    #     print("No threads present")
    #     first_user = request.user
    #     print(first_user)
    #     matches = (
    #         UserTripMatches.objects.values().filter(Q(sender_id="3"))
    #         # .filter(Q(match_status="Pending") | Q(match_status="Matched"))
    #     )
    #     print(matches)
    #     for match in matches:
    #         # print(match["receiver_id"])
    #         second_user = db_retrieve_or_none(User, match["receiver_id"])
    #         print(second_user.id)
    #         if second_user:
    #             t = Thread.objects.get_or_create(
    #                 first_user=first_user, second_user=second_user
    #             )
    #             print(t)
    #             print("Created thread for")
    #             print(first_user)
    #             print(second_user)
    #
    #     # Thread.objects.create()
    return render(request, "chat/threads.html", {"threads": threads})


@login_required
def messages_page(request, thread_id, other_user_id):
    json_data = {
        "thread_id": thread_id,
        "other_user_id": other_user_id,
        "self_user_id": request.user.id,
    }
    print(request.user.id)
    print(other_user_id)
    context = {"dump": json.dumps(json_data)}
    return render(request, "chat/message_room.html", context)
