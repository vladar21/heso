# Generated by Django 4.2.9 on 2024-03-04 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0007_alter_material_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='english_class',
        ),
    ]
