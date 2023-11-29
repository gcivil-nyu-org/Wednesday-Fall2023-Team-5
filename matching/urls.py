from django.urls import path
from .views import (
    show_potential_matches,
    send_matching_request,
    cancel_matching_request,
    show_pending_requests,
    react_pending_request,
    show_matches,
    unmatch
)

app_name = "matching"
urlpatterns = [
    path("show_potential_matches/", show_potential_matches, name="show_potential_matches"),

    path("show_pending_requests/", show_pending_requests, name="show_pending_requests"),

    path("send_match_req/", send_matching_request, name="send_request"),

    path("cancel_match_req/", cancel_matching_request, name="cancel_request"),

    path("react_match_req/", react_pending_request, name="react_request"),

]
