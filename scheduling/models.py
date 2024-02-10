from django.db import models
from django.conf import settings


# Модель EnglishClass представляет учебный класс или курс
class EnglishClass(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_classes',
        limit_choices_to={'is_teacher': True},
        verbose_name="Teacher"
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_classes',
        limit_choices_to={'is_student': True},
        verbose_name="Students"
    )

    class Meta:
        verbose_name = "English Class"
        verbose_name_plural = "English Classes"

    def __str__(self):
        return self.title


# Модель Schedule связывает классы с их расписаниями
class Schedule(models.Model):
    english_class = models.ForeignKey(
        EnglishClass,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name="English Class"
    )
    term = models.CharField(max_length=100, verbose_name="Term")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"

    def __str__(self):
        return f"{self.english_class.title} Schedule"


# Модель Lesson для отдельных занятий
class Lesson(models.Model):
    english_class = models.ForeignKey(
        EnglishClass,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="English Class"
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time")
    google_meet_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Google Meet Link"
    )

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.title


# Модель Material для учебных материалов
class Material(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    type = models.CharField(max_length=100, verbose_name="Type")
    content = models.FileField(
        upload_to='materials/',
        blank=True,
        null=True,
        verbose_name="Content"
    )
    english_class = models.ManyToManyField(
        EnglishClass,
        related_name='materials',
        verbose_name="English Classes"
    )
    lessons = models.ManyToManyField(
        Lesson,
        related_name='materials',
        verbose_name="Lessons"
    )

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def __str__(self):
        return self.title


# Модель GoogleCalendarEvent для событий Google Календаря
class GoogleCalendarEvent(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='google_calendar_events',
        verbose_name="Lesson"
    )
    event_time = models.DateTimeField(verbose_name="Event Time")
    google_event_id = models.CharField(
        max_length=255,
        verbose_name="Google Event ID"
    )

    class Meta:
        verbose_name = "Google Calendar Event"
        verbose_name_plural = "Google Calendar Events"

    def __str__(self):
        return f"Event for {self.lesson.title}"
