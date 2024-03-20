# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that extends the default AbstractUser model.

    Attributes:
        phone_number (models.CharField): Optional field for the user's phone number.
        is_teacher (models.BooleanField): Flag to indicate whether the user is a teacher.
        is_student (models.BooleanField): Flag to indicate whether the user is a student.
        enrollment_date (models.DateField): The date when the user was enrolled.
    """
    # add a phone number field
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Fields to determine if the user is a teacher or a student
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    # Add this line for enrollment date
    enrollment_date = models.DateField(null=True, blank=True)

    class Meta:
        app_label = 'users'
        verbose_name = "General User"

    def __str__(self):
        return self.username
