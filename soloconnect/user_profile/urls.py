from django.urls import path
from . import views

urlpatterns = [
    path('register/1', views.create_user_account, name="register_account"),
    # path('register/2', views.add_matching_preferences, name="add_matching_preferences")
]
