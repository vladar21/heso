# scheduling/apps.py

from django.apps import AppConfig


class SchedulingConfig(AppConfig):
    """
    Configuration class for the 'scheduling' Django application.

    This class sets the default auto field type to 'BigAutoField' for models
    in the 'scheduling' app,
    ensuring that primary keys have enough space to grow without running into
    integer overflow issues.
    It also specifies the app's name, 'scheduling', which Django uses in various
    parts of the framework,
    like when referring to the app in settings or migrations.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "scheduling"
