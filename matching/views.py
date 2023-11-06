from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_profile.models import UserProfile


@login_required
def show_potential_matches(request, trip_id):
    all_user_profiles = UserProfile.objects.all()
    context = {'all_user_profiles': all_user_profiles}
    return render(request, 'matching/list_potential_matches.html', context)
