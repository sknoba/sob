# Generated by Django 5.1.1 on 2024-12-22 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_historicalprofile_experience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprofile',
            name='achivements',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Achivements'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='achivements',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Achivements'),
        ),
    ]