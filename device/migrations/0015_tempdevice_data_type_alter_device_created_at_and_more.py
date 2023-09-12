# Generated by Django 4.1.4 on 2023-03-01 11:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0014_remove_tempdevice_data_type_alter_device_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempdevice',
            name='data_type',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='device',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 1, 17, 2, 22, 672892)),
        ),
        migrations.AlterField(
            model_name='tempdevice',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 1, 17, 2, 22, 672892)),
        ),
    ]