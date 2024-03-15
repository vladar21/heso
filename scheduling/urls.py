# scheduling/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('update-lesson/', views.update_lesson, name='update_lesson'),
    path('classes/', views.english_class_list, name='english_class_list'),
    path('classes/create/', views.create_english_class, name='create_english_class'),
    path('classes/<int:pk>/update/', views.update_english_class, name='update_english_class'),
    path('classes/<int:pk>/delete/', views.delete_english_class, name='delete_english_class'),
    path('lesson_details/', views.lesson_details, name='lesson_details'),
]
