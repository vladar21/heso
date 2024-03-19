# users/apps.py

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for the 'users' application.

    This class configures the 'users' application, specifying
    the default auto field type and the application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
