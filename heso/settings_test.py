# heso/settings_test.py

from .settings import *  # noqa:


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_test.sqlite3",  # noqa:
    }
}
