# Generated by Django 5.1.1 on 2024-12-14 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_alter_student_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mother_mobile_number',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]