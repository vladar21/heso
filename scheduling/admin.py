from django.contrib import admin
from .models import EnglishClass, Schedule, Lesson, Material


@admin.register(EnglishClass)
class EnglishClassAdmin(admin.ModelAdmin):
    """
    Admin interface options for EnglishClass model.

    Defines:
    - Which columns to display in the admin list view ('list_display').
    - How to filter the list view ('list_filter').
    - Which fields to search ('search_fields').
    """
    list_display = ["title", "teacher"]
    list_filter = ["teacher"]
    search_fields = ["title", "description"]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """
    Admin interface options for Schedule model.

    Defines list display, filtering options based on terms and dates, allowing
    administrators to easily navigate through different schedules.
    """
    list_display = ["english_class", "term", "start_date", "end_date"]
    list_filter = ["term", "start_date", "end_date"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin interface options for Lesson model.

    Provides a detailed view on lessons, including filtering and searching capabilities
    to efficiently manage lesson scheduling and details.
    """
    list_display = ["english_class", "title", "start_time", "end_time"]
    list_filter = ["english_class", "start_time", "end_time"]
    search_fields = ["title", "description"]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """
    Admin interface options for Material model.

    Focuses on categorizing materials by type and facilitating the search process through
    titles, enhancing the material management process.
    """
    list_display = ["title", "type"]
    list_filter = ["type"]
    search_fields = ["title"]
