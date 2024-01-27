from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Additional fields
    # add a phone number field
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Fields to determine if the user is a teacher or a student
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Teacher(User):
    department = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)


class Student(User):
    enrollment_date = models.DateField()
    major = models.CharField(max_length=100, blank=True, null=True)
