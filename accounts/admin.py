from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import forms

from accounts.models import CustomUser, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password", "username")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login",'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),  # add "is_staff", "is_active" to be able to set that from admin
            },
        ),
    )
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ("last_login",'date_joined')