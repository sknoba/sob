# Generated by Django 5.1.1 on 2024-12-23 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_historicalprofile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
