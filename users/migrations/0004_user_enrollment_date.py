# Generated by Django 4.2.9 on 2024-03-10 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_teacher_user_ptr_delete_student_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enrollment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
