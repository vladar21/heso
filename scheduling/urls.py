# scheduling/urls.py

from django.urls import path
from . import views

"""
Defines URL patterns for the scheduling application.

The URL patterns include:
- The main schedule page that displays all lessons in a calendar view.
- Functionalities for updating, creating, and deleting lessons and English classes.
- Detailed views for individual lessons and classes, including creation and update forms.
"""


urlpatterns = [
    path("", views.schedule, name="schedule"),
    path("update-lesson/", views.update_lesson, name="update_lesson"),
    path("classes/", views.english_class_list, name="english_class_list"),
    path("classes/create/", views.create_english_class, name="create_english_class"),
    path(
        "classes/<int:pk>/update/",
        views.update_english_class,
        name="update_english_class",
    ),
    path(
        "classes/<int:pk>/delete/",
        views.delete_english_class,
        name="delete_english_class",
    ),
    path("lesson_details/", views.lesson_details, name="lesson_details"),
    path("classes/<int:class_id>/lessons/", views.lessons_list, name="lessons_list"),
    path(
        "classes/<int:class_id>/lessons/create/",
        views.create_lesson,
        name="create_lesson",
    ),
    path(
        "update-lesson/<int:pk>/", views.update_lesson_view, name="update_lesson_view"
    ),
    path("lessons/<int:pk>/delete/", views.delete_lesson, name="delete_lesson"),
]
