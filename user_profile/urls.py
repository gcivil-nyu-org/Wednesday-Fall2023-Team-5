from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "user_profile"
urlpatterns = [
    path("register/", views.create_user_account, name="register_account"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="user_profile/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="user_profile/logout.html"),
        name="logout",
    ),
    path("profile/", views.view_profile, name="view_profile"),
    path("profile/edit", views.edit_profile, name="edit_profile"),
    path("profile/delete", views.milestone_profile, name="milestone_profile"),
]
