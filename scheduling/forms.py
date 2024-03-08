from django import forms
from .models import EnglishClass, Schedule


class EnglishClassForm(forms.ModelForm):
    class Meta:
        model = EnglishClass
        fields = ['title', 'color', 'teacher', 'students']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['term', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'end_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }
        