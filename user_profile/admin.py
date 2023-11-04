from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import UserProfile, UserImages

"""
@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
"""

class UserImagesInline(admin.StackedInline):
    model = UserImages
    max_num = 5
    verbose_name_plural = "User Images"
    fk_name = "user_profile"

@admin.register(UserImages)
class UserImagesAdmin(admin.ModelAdmin):
    pass


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    max_num = 1
    verbose_name_plural = "UserProfiles"
    fk_name = "user"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        UserImagesInline
    ]


class UserAdmin(AuthUserAdmin):
    inlines = [
        UserProfileInline
    ]
