from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from soloconnect import settings

from . import views

app_name = "user_profile"
urlpatterns = [
    path("register/", views.create_user_account, name="register_account"),
    path("login/", views.login_view, name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="user_profile/logout.html"),
        name="logout",
    ),
    path("profile/", views.view_profile, name="view_profile"),
    path("profile/edit", views.edit_profile, name="edit_profile"),
    path("profile/upload/", views.upload_images, name="upload_images"),
    path("profile/delete", views.milestone_profile, name="milestone_profile"),
    path("profile/detail/<int:id>", views.detail_profile, name="detail_profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
