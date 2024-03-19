# heso/settings.py

from pathlib import Path
import os
import dj_database_url

# Importing environment variables if the env.py file exists
if os.path.isfile("env.py"):
    import env


# BASE_DIR represents the directory that contains the manage.py script
# It's used for defining paths to various resources within the project.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: The secret key should not be kept in source code for production environments.
# It's used for cryptographic signing and should be kept secret.
SECRET_KEY = os.environ.get("SECRET_KEY")

# DEBUG mode should be turned off in production for security reasons.
# When True, detailed error pages are shown for exceptions, which can reveal sensitive information.
DEBUG = False

# ALLOWED_HOSTS defines which host/domain names this Django site can serve.
# This is a security measure to prevent HTTP Host header attacks.
ALLOWED_HOSTS = ["127.0.0.1", ".herokuapp.com"]


# INSTALLED_APPS list all Django applications that are activated within this Django instance.
# These apps are used to build the website.
INSTALLED_APPS = [
    # Default Django apps for the admin interface, authentication, sessions, messages, and static files.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Custom apps for user management and scheduling functionality.
    "users",
    "scheduling",
]

# MIDDLEWARE is a framework of hooks into Django's request/response processing.
# It's a lightweight, low-level plugin system for globally altering Django’s input or output.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ROOT_URLCONF points to the Python module that contains the urlpatterns.
ROOT_URLCONF = "heso.urls"

# TEMPLATES configures Django’s template engine.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Directory where the templates are stored.
        "APP_DIRS": True,  # Django will look for a “templates” subdirectory in each of the INSTALLED_APPS.
        "OPTIONS": {
            # Context processors add variables to the context of a template.
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom context processor to add more context.
                "heso.utils.context_processors.add_path_to_context",
            ],
        },
    },
]

# WSGI_APPLICATION points to the WSGI callable that Django uses to get the application object.
WSGI_APPLICATION = "heso.wsgi.application"

# DATABASES configuration includes the connection settings for the default database.
DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}


# AUTH_PASSWORD_VALIDATORS configures validators that are used to check the strength of users’ passwords.
AUTH_PASSWORD_VALIDATORS = [
    # Validators for password strength, similarity to user attributes, commonness, and numeric sequences.
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images) configuration
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Specifies additional directories where Django will look for static files.
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # The absolute path to the directory where collectstatic will

# Default primary key field type for new models
# BigAutoField is a 64-bit integer, much like AutoField except it's guaranteed to fit numbers from 1 to 9223372036854775807.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model specification
# Specifies our custom User model from the 'users' app to be used throughout the project.
AUTH_USER_MODEL = "users.User"

# After login, Django redirects users to the schedule page.
LOGIN_REDIRECT_URL = "/schedule"
# After logout, users are redirected to the login page
LOGOUT_REDIRECT_URL = "/users/login/"
# Defines the URL where requests are redirected for login, especially when using the login_required() decorator.
LOGIN_URL = "/users/login/"

# Email backend configuration
# This setting specifies the backend to use for sending emails.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# Email Use TLS
# True enables the use of Transport Layer Security (TLS) to secure the connection with the mail server.
EMAIL_USE_TLS = True
# Email Host
# The host used for sending email. For example, 'smtp.gmail.com' for Gmail. 'sandbox.smtp.mailtrap.io' is used here for a mailtrap.io sandbox.
EMAIL_HOST = "sandbox.smtp.mailtrap.io"
# Email Host User
# Username to use for the SMTP server defined in EMAIL_HOST. Typically provided by your email service.
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# Email Host Password
# Password to use for the SMTP server defined in EMAIL_HOST. Typically provided by your email service.
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# Email Port
# Port to use for the SMTP server defined in EMAIL_HOST.
EMAIL_PORT = "2525"
