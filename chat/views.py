import json

# import logging

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# from common import db_retrieve_or_none
# from matching.models import UserTripMatches

# from common import db_retrieve_or_none
# from matching.models import UserTripMatches
from .models import Thread, ChatMessage
from django.db.models import Q


@login_required
def threads_page(request):
    threads = (
        Thread.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
        .prefetch_related("chat_message")
        .order_by("timestamp")
    )
    # if not threads:
    #     print("No threads present")
    #     first_user = request.user
    #     print(first_user)
    #     matches = UserTripMatches.objects.values().filter(Q(match_status="Matched"))
    #     print(matches)
    #     for match in matches:
    #         print("sender id: ")
    #         print(match["sender_id"])
    #         print("receiver id: ")
    #         print(match["receiver_id"])
    #         print("request_id: ")
    #         print(request.user.id)
    #         if request.user.id == match["sender_id"]:
    #             second_user = db_retrieve_or_none(User, match["receiver_id"])
    #             print("second_user: ")
    #             print(second_user.id)
    #             if second_user:
    #                 if second_user.id != first_user.id:
    #                     t = Thread.objects.get_or_create(
    #                         first_user=first_user, second_user=second_user
    #                     )
    #                 #         # print(t)
    #                     print("Created thread for")
    #                     print(first_user)
    #                     print(second_user)

    # Thread.objects.create()
    return render(request, "chat/threads.html", {"threads": threads})


@login_required
def messages_page(request, thread_id, other_user_id):

    threads = (
        Thread.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
        .prefetch_related("chat_message")
        .order_by("timestamp")
    )

    message_history = ChatMessage.objects.filter(thread=thread_id)

    json_data = {
        "thread_id": thread_id,
        "other_user_id": other_user_id,
        "self_user_id": request.user.id,
    }

    other_user = User.objects.get(id=other_user_id)

    chat_data = {
        "thread_id": thread_id,
        "other_user_instance": other_user
    }

    print(request.user.id)
    print(other_user_id)

    context = {
        "dump": json.dumps(json_data),
        "chat_data": chat_data,
        "message_history": message_history,
        "threads": threads,
    }

    return render(request, "chat/message_room.html", context)
