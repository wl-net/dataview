from django.db import models
import datetime

class SensorType(models.Model):
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Sensor(models.Model):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(SensorType)
    description = models.TextField(blank=True)
    location = models.ForeignKey('portal.Room')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class SensorValue(models.Model):
    sensor = models.ForeignKey('sensors.Sensor')
    updated = models.DateTimeField(auto_now_add=True, blank=True)
    value = models.TextField()

    def __unicode__(self):
        return self.sensor + " " + self.updated

    def __str__(self):
        return self.sensor + " " + self.updated
