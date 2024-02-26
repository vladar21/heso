from django.urls import path
from . import views


urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('update-lesson/', views.update_lesson, name='update_lesson'),
]
