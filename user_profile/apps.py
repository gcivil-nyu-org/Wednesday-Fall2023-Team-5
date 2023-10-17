from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_profile"

    def ready(self):
        # DISCLAIMER Do not comment out the below line it will break so many things
        from .import signals
