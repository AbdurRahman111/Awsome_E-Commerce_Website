# Generated by Django 3.1.4 on 2021-01-09 17:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicifyapp', '0006_auto_20210109_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 1, 9, 23, 16, 33, 876396)),
        ),
        migrations.AlterField(
            model_name='posted_jobs',
            name='post_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 1, 9, 23, 16, 33, 875397)),
        ),
        migrations.AlterField(
            model_name='product_details',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/product_image'),
        ),
        migrations.AlterField(
            model_name='product_details',
            name='image2',
            field=models.ImageField(null=True, upload_to='uploads/product_image'),
        ),
        migrations.AlterField(
            model_name='product_details',
            name='image3',
            field=models.ImageField(null=True, upload_to='uploads/product_image'),
        ),
        migrations.AlterField(
            model_name='product_details',
            name='image4',
            field=models.ImageField(null=True, upload_to='uploads/product_image'),
        ),
        migrations.AlterField(
            model_name='product_details',
            name='image5',
            field=models.ImageField(null=True, upload_to='uploads/product_image'),
        ),
    ]
