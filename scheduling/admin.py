from django.contrib import admin
from .models import EnglishClass, Schedule, Lesson, Material


# Регистрация модели EnglishClass
@admin.register(EnglishClass)
class EnglishClassAdmin(admin.ModelAdmin):
    list_display = ["title", "teacher"]
    list_filter = ["teacher"]
    search_fields = ["title", "description"]


# Регистрация модели Schedule
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["english_class", "term", "start_date", "end_date"]
    list_filter = ["term", "start_date", "end_date"]


# Регистрация модели Lesson
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["english_class", "title", "start_time", "end_time"]
    list_filter = ["english_class", "start_time", "end_time"]
    search_fields = ["title", "description"]


# Регистрация модели Material
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["title", "type"]
    list_filter = ["type"]
    search_fields = ["title"]
