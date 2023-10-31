from django.urls import path
from . import views

app_name = "trip"
urlpatterns = [
    path("trip/view/", views.view_trips, name="view_trips"),
    path("trip/create/", views.create_trip, name="create_trip"),
    path("trip/view/<int:id>", views.detail_trip, name="detail_trip"),
]
