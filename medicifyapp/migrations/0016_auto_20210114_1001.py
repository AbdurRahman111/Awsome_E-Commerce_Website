# Generated by Django 3.1.4 on 2021-01-14 04:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicifyapp', '0015_auto_20210113_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 1, 14, 10, 1, 29, 711915)),
        ),
        migrations.AlterField(
            model_name='posted_jobs',
            name='post_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 1, 14, 10, 1, 29, 710916)),
        ),
    ]