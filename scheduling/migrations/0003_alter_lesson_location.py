# Generated by Django 4.2.9 on 2024-02-11 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0002_lesson_location_lesson_online_meeting_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='location',
            field=models.CharField(choices=[('on-site', 'On-site'), ('on-line', 'On-line')], default='on-site', max_length=10, verbose_name='location'),
        ),
    ]