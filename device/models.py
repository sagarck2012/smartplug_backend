import datetime
import uuid

from django.db import models


# Create your models here.

class DeviceReg(models.Model):
    device_id = models.CharField(null=False, max_length=255, unique=True)
    location = models.CharField(null=False, max_length=255)
    sensor_id = models.CharField(null=True, max_length=255)
    status = models.CharField(null=True, default="Disconnected", max_length=50)
    yesterday_total = models.FloatField(null=True, blank=True)
    today_total = models.FloatField(null=True, blank=True)

    # installed_by = models.CharField(null=True, max_length=255)

    class Meta:
        db_table = 'device_reg'


class DeviceConnection(models.Model):
    value = models.CharField(null=False, max_length=128)

    class Meta:
        db_table = 'device_connection'


class Device(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now())
    device_detail = models.ForeignKey(DeviceReg, on_delete=models.CASCADE)
    device_id = models.CharField(null=False, max_length=255)
    energy_consumption = models.IntegerField(default=0)
    is_connected = models.ForeignKey(DeviceConnection, on_delete=models.CASCADE, default=1)
    is_powered = models.BooleanField(default=1)
    data_type = models.BooleanField(null=False, default=1)
    total_consumption = models.FloatField(default=0.000)
    # device_connectivity = models.BooleanField(default=True)

    class Meta:
        # ordering = ['timestamp']
        db_table = 'device_data'


class TempDevice(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now())
    device_detail = models.ForeignKey(DeviceReg, on_delete=models.CASCADE)
    device_id = models.CharField(null=False, max_length=255)
    energy_consumption = models.IntegerField(default=0)
    is_connected = models.ForeignKey(DeviceConnection, on_delete=models.CASCADE, default=1)
    is_powered = models.BooleanField(default=1)
    data_type = models.BooleanField(null=False, default=1)
    total_consumption = models.FloatField(default=0.000)
    # device_connectivity = models.BooleanField(default=True)

    class Meta:
        # ordering = ['timestamp']
        db_table = 'temp_device_data'


class ActualDeviceData(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now())
    device_detail = models.ForeignKey(DeviceReg, on_delete=models.CASCADE)
    device_id = models.CharField(null=False, max_length=255)
    energy_consumption = models.IntegerField(default=0)
    is_connected = models.ForeignKey(DeviceConnection, on_delete=models.CASCADE, default=1)
    is_powered = models.BooleanField(default=1)
    data_type = models.BooleanField(null=False, default=1)
    total_consumption = models.FloatField(default=0.000)
    # device_connectivity = models.BooleanField(default=True)

    class Meta:
        # ordering = ['timestamp']
        db_table = 'actual_device_data'



class SummaryData(models.Model):
    created_at = models.DateField(default=datetime.date.today())
    device_detail = models.ForeignKey(DeviceReg, on_delete=models.CASCADE)
    device_id = models.CharField(null=False, max_length=255)
    total_consumption = models.FloatField(default=0.000)

    class Meta:
        # ordering = ['timestamp']
        db_table = 'summary_data'
