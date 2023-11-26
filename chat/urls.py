from django.urls import path

from .views import trip_messages_page

app_name = "chat"
urlpatterns = [
    path("", trip_messages_page, name="trip_messages_page"),
]
