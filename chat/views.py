import json
# import logging

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

# from user_profile.models import UserProfile, UserImages

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
        .order_by("updated")
    )
    ou_id = None
    if threads:
        to_pass = threads[0]
        if request.user == to_pass.first_user:
            ou_id = to_pass.second_user.id
        else:
            ou_id = to_pass.first_user.id
    else:
        to_pass = None

    if to_pass:
        return redirect(reverse('chat:messages_page', kwargs={'thread_id': to_pass.id, 'other_user_id': ou_id}))
    else:
        return redirect(reverse('chat:messages_page_empty'))


@login_required
def messages_page_empty(request):
    return render(request, 'chat/message_room.html', {})


@login_required
def messages_page(request, thread_id, other_user_id):
    threads = (
        Thread.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
        .prefetch_related("chat_message")
        .order_by("timestamp")
    )

    message_history = ChatMessage.objects.filter(thread=thread_id)
    thread_instances = [Thread(**item) for item in threads.values()]

    print(message_history.values())
    other_user = User.objects.get(id=other_user_id)

    sender_image_url = ""
    receiver_image_url = ""

    if len(thread_instances) > 0:
        if thread_instances[0].first_user == request.user:
            sender_image_url = thread_instances[0].first_user_image_url
            receiver_image_url = thread_instances[0].second_user_image_url
        else:
            sender_image_url = thread_instances[0].second_user_image_url
            receiver_image_url = thread_instances[0].first_user_image_url

    json_data = {
        "thread_id": thread_id,
        "other_user_id": other_user_id,
        "self_user_id": request.user.id,
        "sender_image_url": sender_image_url,
        "receiver_image_url": receiver_image_url,
    }
    chat_data = {"thread_id": thread_id, "other_user_instance": other_user}

    print(request.user.id)
    print(sender_image_url)
    print(other_user_id)
    print(receiver_image_url)
    context = {
        "dump": json.dumps(json_data),
        "chat_data": chat_data,
        "message_history": message_history,
        "threads": threads,
    }

    return render(request, "chat/message_room.html", context)
