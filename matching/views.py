from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User
from user_profile.models import UserProfile

# from .models import UserTripMatches


@login_required
def show_potential_matches(request, trip_id):
    all_user_profiles = UserProfile.objects.all()
    context = {"all_user_profiles": all_user_profiles}
    return render(request, "matching/list_potential_matches.html", context)


@login_required
def send_matching_request(request, trip_id, receiver_id):
    pass


@login_required
def cancel_matching_request(request, trip_id, receiver_id):
    pass


@login_required
def unmatch_user(request, trip_id, receiver_id):
    pass


@login_required
def approve_matching_request(request, trip_id, sender_id):
    pass
