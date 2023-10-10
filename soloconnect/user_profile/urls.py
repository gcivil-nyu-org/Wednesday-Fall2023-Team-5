from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_user_account, name="register_account"),
]
