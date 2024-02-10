# Generated by Django 4.2.9 on 2024-02-10 21:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('students', models.ManyToManyField(limit_choices_to={'is_student': True}, related_name='enrolled_classes', to=settings.AUTH_USER_MODEL, verbose_name='Students')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_teacher': True}, on_delete=django.db.models.deletion.CASCADE, related_name='taught_classes', to=settings.AUTH_USER_MODEL, verbose_name='Teacher')),
            ],
            options={
                'verbose_name': 'English Class',
                'verbose_name_plural': 'English Classes',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('start_time', models.DateTimeField(verbose_name='Start Time')),
                ('end_time', models.DateTimeField(verbose_name='End Time')),
                ('google_meet_link', models.URLField(blank=True, null=True, verbose_name='Google Meet Link')),
                ('english_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='scheduling.englishclass', verbose_name='English Class')),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=100, verbose_name='Term')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('english_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='scheduling.englishclass', verbose_name='English Class')),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
                ('content', models.FileField(blank=True, null=True, upload_to='materials/', verbose_name='Content')),
                ('english_class', models.ManyToManyField(related_name='materials', to='scheduling.englishclass', verbose_name='English Classes')),
                ('lessons', models.ManyToManyField(related_name='materials', to='scheduling.lesson', verbose_name='Lessons')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materials',
            },
        ),
        migrations.CreateModel(
            name='GoogleCalendarEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_time', models.DateTimeField(verbose_name='Event Time')),
                ('google_event_id', models.CharField(max_length=255, verbose_name='Google Event ID')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='google_calendar_events', to='scheduling.lesson', verbose_name='Lesson')),
            ],
            options={
                'verbose_name': 'Google Calendar Event',
                'verbose_name_plural': 'Google Calendar Events',
            },
        ),
    ]
