# Generated by Django 5.1.1 on 2024-11-14 05:30

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='teacher_id',
            field=models.CharField(default=core.models.generate_id, max_length=20, null=True, unique=True),
        ),
    ]