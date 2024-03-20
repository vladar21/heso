# scheduling/models.py

import hashlib
from django.db import models
from django.conf import settings
from django.utils import timezone


def generate_hsl_color(unique_identifier, saturation=100, lightness=30):
    """
    Generate a unique HSL color based on a unique identifier.

    Args:
    - unique_identifier: A unique string to base
    the color on (e.g., class title).
    - saturation: Saturation percentage of the color (default: 100).
    - lightness: Lightness percentage of the color (default: 30).

    Returns:
    - A string representing an HSL color.
    """
    # Convert the unique identifier to a hash value to get a pseudo-random number
    hash_value = int(hashlib.sha256(unique_identifier.encode("utf-8")).hexdigest(), 16)
    # Use the hash value to generate a hue value between 0 and 360
    hue = hash_value % 360
    # Return the HSL color string
    return f"hsl({hue}, {saturation}%, {lightness}%)"


def check_color_uniqueness(color, used_colors):
    """
    Check if the generated color is unique.

    Args:
    - color: The generated HSL color string.
    - used_colors: A list of already used colors.

    Returns:
    - True if the color is unique, False otherwise.
    """
    return color not in used_colors


class EnglishClass(models.Model):
    """
    Represents a classroom or a course, including its title, description, associated color,
    teacher, and enrolled students.

    Attributes:
        title (models.CharField): The title of the English class.
        description (models.TextField): A brief description of the class.
        color (models.CharField): A color associated with the class, used for UI distinction.
        teacher (models.ForeignKey): A reference to the User model, specifically for users
        marked as teachers.
        students (models.ManyToManyField): A many-to-many relationship to the User model for
        users marked as students.
    """
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    color = models.CharField(max_length=20, default="#FFFFFF")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="taught_classes",
        limit_choices_to={"is_teacher": True},
        verbose_name="Teacher",
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="enrolled_classes",
        limit_choices_to={"is_student": True},
        verbose_name="Students",
    )

    class Meta:
        app_label = 'scheduling'
        verbose_name = "English Class"
        verbose_name_plural = "English Classes"

    def save(self, *args, **kwargs):
        if not self.color or self.color == "#FFFFFF":
            # Getting the colours already used
            used_colors = set(
                EnglishClass.objects.exclude(id=self.id).values_list("color", flat=True)
            )
            # Generating a unique colour
            new_color = generate_hsl_color(self.title)
            while new_color in used_colors:
                # Generate a new colour if the found colour is already used
                new_color = generate_hsl_color(self.title + str(len(used_colors)))
            self.color = new_color
        super().save(*args, **kwargs)

    def number_of_students(self):
        """Returns the number of students enrolled in the class."""
        return self.students.count()

    def upcoming_lessons(self):
        """Returns upcoming lessons for the class."""
        return self.lessons.filter(start_time__gt=timezone.now(), status="planned")

    def __str__(self):
        return self.title


class Schedule(models.Model):
    """
    Associates an EnglishClass with a specific schedule, including the term and start/end dates.

    Attributes:
        english_class (models.ForeignKey): A reference to the associated EnglishClass.
        term (models.CharField): The term during which this class is scheduled (e.g., Spring 2024).
        start_date (models.DateField): The start date of the class.
        end_date (models.DateField): The end date of the class.
    """
    english_class = models.ForeignKey(
        EnglishClass,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="English Class",
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


class Lesson(models.Model):
    """
    Represents an individual lesson associated with an EnglishClass, detailing the lesson's timing,
    location, and status.

    Attributes:
        english_class (models.ForeignKey): The English class this lesson belongs to.
        title (models.CharField): The title of the lesson.
        description (models.TextField): A detailed description of the lesson's content.
        start_time (models.DateTimeField): When the lesson starts.
        end_time (models.DateTimeField): When the lesson ends.
        meeting_link (models.URLField): An optional link for online lessons.
        location (models.CharField): The location of the lesson, either on-site or online.
        status (models.CharField): The current status of the lesson (planned, completed, cancelled).
    """
    english_class = models.ForeignKey(
        EnglishClass,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="English Class",
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time")
    meeting_link = models.URLField(blank=True, null=True, verbose_name="Meeting Link")
    LOCATION_CHOICES = [
        ("on-site", "On-site"),
        ("on-line", "On-line"),
    ]
    location = models.CharField(
        max_length=10,
        choices=LOCATION_CHOICES,
        default="on-site",
        verbose_name="location",
    )
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="planned", verbose_name="Status"
    )

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def is_upcoming(self):
        """Checks if the lesson is upcoming."""
        return self.start_time > timezone.now() and self.status == "planned"

    def is_completed(self):
        """Checks if the lesson is completed."""
        return self.end_time < timezone.now() and self.status == "completed"

    def is_cancelled(self):
        """Checks if the lesson is cancelled."""
        return self.status == "cancelled"

    def duration(self):
        """Returns the duration of the lesson."""
        return self.end_time - self.start_time

    def __str__(self):
        return self.title


class Material(models.Model):
    """
    Represents educational materials associated with lessons, including type and content.

    Attributes:
        title (models.CharField): The title of the material.
        type (models.CharField): The type of material (e.g., book, video, article).
        content (models.BinaryField): The binary content of the material, suitable for file storage.
        lessons (models.ManyToManyField): Lessons that utilize this material.
    """
    title = models.CharField(max_length=255, verbose_name="Title")
    type = models.CharField(max_length=100, verbose_name="Type")
    content = models.BinaryField(blank=True, null=True, verbose_name="Content")

    lessons = models.ManyToManyField(
        Lesson, related_name="materials", verbose_name="Lessons"
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
