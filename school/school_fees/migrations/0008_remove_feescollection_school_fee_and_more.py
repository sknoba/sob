# Generated by Django 5.1.1 on 2024-12-13 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_fees', '0007_feescollection_school_fee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feescollection',
            name='school_fee',
        ),
        migrations.RemoveField(
            model_name='feescollection',
            name='transport_fee',
        ),
        migrations.RemoveField(
            model_name='historicalfeescollection',
            name='school_fee',
        ),
        migrations.RemoveField(
            model_name='historicalfeescollection',
            name='transport_fee',
        ),
    ]