# Generated by Django 4.2.9 on 2024-02-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='online_meeting_link',
            field=models.URLField(blank=True, null=True, verbose_name='Online Meeting Link'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('planned', 'Planned'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned', max_length=10, verbose_name='Status'),
        ),
    ]