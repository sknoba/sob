# Generated by Django 5.1.1 on 2024-12-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_alter_student_father_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='father_age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]