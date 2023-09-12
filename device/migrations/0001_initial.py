# Generated by Django 4.1.4 on 2023-01-01 11:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'device_connection',
            },
        ),
        migrations.CreateModel(
            name='DeviceReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'device_reg',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('device_id', models.CharField(max_length=255)),
                ('energy_consumption', models.IntegerField(default=0)),
                ('device_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.devicereg')),
                ('is_connected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.deviceconnection')),
            ],
            options={
                'db_table': 'device_data',
                'ordering': ['timestamp'],
            },
        ),
    ]