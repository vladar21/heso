from django import forms
from django.contrib.auth import get_user_model
from multiupload.fields import MultiFileField
from .models import EnglishClass, Schedule, Lesson, Material


User = get_user_model()


class EnglishClassForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(is_teacher=True),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_student=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = EnglishClass
        fields = ["title", "color", "description", "teacher", "students"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(EnglishClassForm, self).__init__(*args, **kwargs)

        if user and not user.is_superuser:
            self.fields["teacher"].disabled = True


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["term", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(format=("%Y-%m-%d"), attrs={"type": "date"}),
            "end_date": forms.DateInput(format=("%Y-%m-%d"), attrs={"type": "date"}),
        }


class LessonForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(is_teacher=True),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_student=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    materials = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    new_materials = MultiFileField(
        min_num=False, max_num=5, max_file_size=1024 * 1024 * 5
    )

    class Meta:
        model = Lesson
        fields = [
            "title",
            "description",
            "start_time",
            "end_time",
            "location",
            "meeting_link",
            "teacher",
            "students",
            "materials",
            "new_materials",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "start_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "location": forms.Select(attrs={"class": "form-control"}),
            "meeting_link": forms.URLInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["teacher"].initial = self.instance.english_class.teacher
            self.fields["students"].initial = self.instance.english_class.students.all()
            self.fields["materials"].initial = self.instance.materials.all()

    def save(self, commit=True):
        lesson = super(LessonForm, self).save(commit=False)

        if commit:
            lesson.save()
            self.save_m2m()

        return lesson
