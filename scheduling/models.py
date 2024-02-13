from django.db import models
from django.conf import settings
from django.utils import timezone
import random


# Example set of 30 dark colors
DARK_COLORS = [
    '#00416A', '#1A1A1D', '#0A0F0D', '#4B0082', '#002635', 
    '#2C3531', '#123456', '#2A2B2D', '#343837', '#3B3C36',
    '#413839', '#3D3E40', '#464646', '#484848', '#494949',
    '#4C4F50', '#4F4A4A', '#515151', '#525252', '#555555',
    '#565051', '#5B5A5A', '#5C5B5B', '#5D5D5D', '#616569',
    '#626D6D', '#646464', '#666362', '#696969', '#6E6A6B'
]


def generate_unique_dark_color(excluded_colors):
    """
    Generates a unique dark color that's not in the excluded_colors list.
    """
    available_colors = [color for color in DARK_COLORS if color not in excluded_colors]
    if not available_colors:  # If all colors are used, fallback to a random choice or handle differently
        return random.choice(DARK_COLORS)
    return random.choice(available_colors)


# Модель EnglishClass представляет учебный класс или курс
class EnglishClass(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    color = models.CharField(max_length=7, default='#FFFFFF')
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

    def save(self, *args, **kwargs):
        if not self.color or self.color == '#FFFFFF':  # If color not set
            # Fetch already used colors
            used_colors = list(EnglishClass.objects.values_list('color', flat=True))
            self.color = generate_unique_dark_color(used_colors)
        super(EnglishClass, self).save(*args, **kwargs)

    def number_of_students(self):
        """Returns the number of students enrolled in the class."""
        return self.students.count()
    
    def upcoming_lessons(self):
        """Returns upcoming lessons for the class."""
        return self.lessons.filter(
            start_time__gt=timezone.now(), status='planned')

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

    def schedule_duration(self):
        """Calculates the duration of the schedule."""
        return self.end_date - self.start_date
    
    def current_term(self):
        """Checks if the schedule is for the current term."""
        current_date = timezone.now().date()
        return self.start_date <= current_date <= self.end_date

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
    LOCATION_CHOICES = [
        ('on-site', 'On-site'),
        ('on-line', 'On-line'),
    ]
    location = models.CharField(
        max_length=10,
        choices=LOCATION_CHOICES, default='on-site', verbose_name="location")
    # location = models.CharField(
    #     max_length=255, blank=True, null=True, verbose_name="Location")
    online_meeting_link = models.URLField(
        blank=True, null=True, verbose_name="Online Meeting Link")
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES, default='planned', verbose_name="Status")

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
    
    def is_upcoming(self):
        """Checks if the lesson is upcoming."""
        return self.start_time > timezone.now() and self.status == 'planned'

    def is_completed(self):
        """Checks if the lesson is completed."""
        return self.end_time < timezone.now() and self.status == 'completed'

    def is_cancelled(self):
        """Checks if the lesson is cancelled."""
        return self.status == 'cancelled'

    def duration(self):
        """Returns the duration of the lesson."""
        return self.end_time - self.start_time

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
    
    def associated_classes(self):
        """Returns classes associated with the material."""
        return self.english_classes.all()
    
    def associated_lessons(self):
        """Returns lessons that use the material."""
        return self.lessons.all()

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
    
    def event_details(self):
        """Returns detailed information about the calendar event."""
        return f"Event for lesson: {self.lesson.title} at {self.event_time}"

    def is_past_event(self):
        """Checks if the event has already occurred."""
        return self.event_time < timezone.now()

    def __str__(self):
        return f"Event for {self.lesson.title}"
