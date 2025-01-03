# Generated by Django 5.1.1 on 2024-12-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0004_alter_examscore_note_alter_historicalexamscore_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exams',
            name='exam',
            field=models.CharField(choices=[('p1', 'Periodic Test 1'), ('p2', 'Periodic Test 2'), ('t1', 'Term Examination 1'), ('t2', 'Term Examination 2')], max_length=10),
        ),
        migrations.AlterField(
            model_name='historicalexams',
            name='exam',
            field=models.CharField(choices=[('p1', 'Periodic Test 1'), ('p2', 'Periodic Test 2'), ('t1', 'Term Examination 1'), ('t2', 'Term Examination 2')], max_length=10),
        ),
    ]
