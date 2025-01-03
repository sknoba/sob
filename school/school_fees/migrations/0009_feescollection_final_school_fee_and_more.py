# Generated by Django 5.1.1 on 2024-12-13 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_fees', '0008_remove_feescollection_school_fee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feescollection',
            name='final_school_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='feescollection',
            name='final_transport_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='historicalfeescollection',
            name='final_school_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='historicalfeescollection',
            name='final_transport_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
