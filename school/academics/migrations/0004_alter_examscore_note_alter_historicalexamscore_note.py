# Generated by Django 5.1.1 on 2024-12-18 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0003_alter_exams_note_alter_historicalexams_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examscore',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalexamscore',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
