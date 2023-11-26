from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Thread

@login_required
def trip_messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chat_message').order_by('timestamp')
    return render(request, 'chat/room.html', {"threads": threads})