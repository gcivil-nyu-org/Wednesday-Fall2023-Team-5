from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

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
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            email_template_name="user_profile/password_reset_email.html",
            success_url="/reset_password_sent/",
            template_name="user_profile/password_reset_form.html",
            subject_template_name="user_profile/password_reset_subject.txt",
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="user_profile/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url="/reset_password_complete/",
            template_name="user_profile/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user_profile/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

