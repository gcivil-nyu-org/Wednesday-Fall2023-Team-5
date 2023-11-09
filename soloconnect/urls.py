"""
URL configuration for soloconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

handler403 = "home_default.views.custom_403"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home_default.urls")),
    path("", include("user_profile.urls")),
    path("", include("trip.urls")),
    path("trip/view/<int:trip_id>/", include("matching.urls")),
]
