# Generated by Django 5.1.1 on 2024-11-17 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0002_enrollment_standard_alter_enrollment_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrollment',
            old_name='date',
            new_name='enrollment_date',
        ),
    ]
