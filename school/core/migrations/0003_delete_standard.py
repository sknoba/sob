# Generated by Django 5.1.1 on 2024-12-10 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_standard_class_teacher_class'),
        ('student', '0003_alter_enrollment_standard'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Standard',
        ),
    ]