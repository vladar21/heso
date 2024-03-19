# users/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


# Unregister the default Group model from admin as it might not be used
admin.site.unregister(Group)


class CustomUserAdmin(BaseUserAdmin):
    """
    A custom UserAdmin class that defines the admin interface for the User model.

    This class customizes how the User model appears in the Django admin interface,
    including which fields are displayed and how they are organized.
    """
    # Define the fields to be displayed in the admin form and their grouping
    fieldsets = (
        (None, {"fields": ("username", "password", "is_teacher", "is_student")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    # Define fields to be used when adding a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    # Specify fields to be displayed in the user list
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_teacher",
        "is_student",
    )
    # Specify fields to be used in search queries
    search_fields = ("username", "email", "first_name", "last_name")
    # Define the default ordering of user records
    ordering = ("username",)

    class Media:
        """
        Defines custom media to be included in the admin.
        """
        js = ("../static/js/script.js",)


# Filter out 'groups' and 'user_permissions' from the fieldsets as they might not be needed
CustomUserAdmin.fieldsets = list(
    filter(
        lambda x: "groups" not in x[1]["fields"]
        and "user_permissions" not in x[1]["fields"],
        CustomUserAdmin.fieldsets,
    )
)


# Register the custom User model and the CustomUserAdmin with the admin site
admin.site.register(User, CustomUserAdmin)
