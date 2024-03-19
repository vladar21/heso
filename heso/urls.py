# heso/urls.py

from django.contrib import admin
from django.urls import path, include
from users.views import home


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("schedule/", include("scheduling.urls")),
    path("users/", include("users.urls")),
]
