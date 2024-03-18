from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_teacher', 'is_student')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_teacher', 'is_student')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    class Media:
        js = (
            '../static/js/script.js',
        )


CustomUserAdmin.fieldsets = list(filter(lambda x: 'groups' not in x[1]['fields'] and 'user_permissions' not in x[1]['fields'], CustomUserAdmin.fieldsets))

admin.site.register(User, CustomUserAdmin)
