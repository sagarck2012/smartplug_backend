# Generated by Django 4.1.4 on 2023-01-25 04:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0006_devicereg_last_time_devicereg_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 25, 10, 51, 24, 943715)),
        ),
        migrations.AlterField(
            model_name='devicereg',
            name='status',
            field=models.CharField(default='Disconnected', max_length=50),
        ),
    ]
