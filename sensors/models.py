from django.db import models

class SensorType(models.Model):
    name = models.CharField(max_length=128)
    
class Sensor(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Residence')

class SensorValue(models.Model):
    sensor = models.ForeignKey('sensors.Sensor')
    updated = models.DateTimeField()
    value = models.TextField()
