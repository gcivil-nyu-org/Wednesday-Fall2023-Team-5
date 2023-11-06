from django.urls import path
from .views import show_potential_matches

app_name = "matching"
urlpatterns = [
    # The respected view function should return list of user matches,
    # they'll have the current user_id, trip_id against which they want to see
    # list of other user matches
    path('show_matches/', show_potential_matches, name="show_potential_matches"),

    # The respected view function should create a matching request in the
    # UserTripMatch model if it's not already there.
    # path('<int:trip_id>/send_match_req/<int:receiver_id>/'),

    # This should handle the updates on any given match
    # path('<int:trip_id>/update_match_req/<int:receiver_id>/<str:match_status>'),

    # This should display all the pending matching requests
    # path('<int:trip_id>/show_pending_req/'),
]
