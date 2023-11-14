from django.urls import path
from .views import show_potential_matches, send_matching_request, cancel_matching_request

app_name = "matching"
urlpatterns = [
    # The respected view function should return list of user matches,
    # they'll have the current user_id, trip_id against which they want to see
    # list of other user matches
    path("show_matches/", show_potential_matches,
         name="show_potential_matches"),

    # path("show_pending_requests/", name="show_pending_requests"),

    # The respected view function should create a matching request in the
    # UserTripMatch model if it's not already there.
    path('send_match_req/<int:receiver_uid>/', send_matching_request,
         name="send_request"),

    path('cancel_match_req/<int:receiver_uid>/', cancel_matching_request,
         name="cancel_request"),

    # path('accept_match_req/<int:sender_uid>/', name="accept_request"),

    # path('reject_match/req/<int:sender_uid>/', name="reject_request"),
]
