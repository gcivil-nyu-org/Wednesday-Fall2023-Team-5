import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Thread


@login_required
def threads_page(request):
    threads = (
        Thread.objects.by_user(user=request.user)
        .prefetch_related("chat_message")
        .order_by("timestamp")
    )
    return render(request, "chat/threads.html", {"threads": threads})

@login_required
def messages_page(request, thread_id, other_user_id):
    json_data = {
        "thread_id": thread_id,
        "other_user_id": other_user_id,
        "self_user_id": request.user.id
    }
    context = {
        "jsonData": json.dumps(json_data)
    }
    return render(request, "chat/")