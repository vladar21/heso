from django.contrib import admin
from .models import User, Teacher, Student


# Custom admin class for User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_teacher', 'is_student']
    # You can add more customizations here


# Custom admin class for Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['username', 'department', 'bio']
    # Additional customizations


# Custom admin class for Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'enrollment_date', 'major']
    # Further customizations
