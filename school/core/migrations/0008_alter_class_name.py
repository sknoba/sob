# Generated by Django 5.1.1 on 2024-12-16 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_class_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(help_text='Class 1st etc...', max_length=50),
        ),
    ]
