# Generated by Django 5.1.1 on 2024-11-17 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_rename_enrollment_date_student_create_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='standard',
        ),
    ]