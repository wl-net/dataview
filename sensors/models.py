from django.db import models
from dataview.models import UUIDModel

class SensorType(UUIDModel):
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Sensor(UUIDModel):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(SensorType)
    description = models.TextField(blank=True)
    location = models.ForeignKey('building.Room', null=True, blank=True)

    def get_most_recent_value(self):
        return SensorValue.objects.filter(sensor=self).order_by('-updated')[0].value

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class SensorValue(UUIDModel):
    sensor = models.ForeignKey('sensors.Sensor')
    updated = models.DateTimeField(auto_now_add=True, blank=True)
    value = models.TextField()

    def __unicode__(self):
        return self.sensor + " " + self.updated

    def __str__(self):
        return self.sensor + " " + self.updated
