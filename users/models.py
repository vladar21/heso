# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Additional fields
    # add a phone number field
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Fields to determine if the user is a teacher or a student
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    # Add this line for enrollment date
    enrollment_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "General User"

    def __str__(self):
        return self.username
