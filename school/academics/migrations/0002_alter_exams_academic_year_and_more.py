# Generated by Django 5.1.1 on 2024-12-18 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
        ('core', '0008_alter_class_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exams',
            name='academic_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.academicyear'),
        ),
        migrations.AlterField(
            model_name='historicalexams',
            name='academic_year',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.academicyear'),
        ),
    ]