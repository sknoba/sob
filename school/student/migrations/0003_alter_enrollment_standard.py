# Generated by Django 5.1.1 on 2024-12-10 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_standard_class_teacher_class'),
        ('student', '0002_alter_student_permanent_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='core.class'),
        ),
    ]
