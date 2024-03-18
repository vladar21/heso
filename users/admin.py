from django.contrib import admin
from .models import User


# Custom admin class for User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_teacher', 'is_student']
    # You can add more customizations here
