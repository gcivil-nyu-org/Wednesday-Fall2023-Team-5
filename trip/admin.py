from django.contrib import admin  # noqa

from trip.models import Trip, UserTrip

# Register your models here.

admin.site.register(Trip)
admin.site.register(UserTrip)