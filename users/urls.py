# users/urls.py

from django.urls import path
from .views import LoginView, register, custom_logout


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register, name='register'),
]
