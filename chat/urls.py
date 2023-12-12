from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path("", views.threads_page, name="threads_page"),
    path(
        "thread/<int:thread_id>/<int:other_user_id>",
        views.messages_page,
        name="messages_page",
    ),
    path(
        "thread/",
        views.messages_page_empty,
        name="messages_page_empty",
    ),
]
