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
    type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    location = models.ForeignKey('building.Room', null=True, blank=True, on_delete=models.CASCADE)

    def get_values(self, count=10):
        return SensorValue.objects.filter(sensor=self).order_by('-updated')[:count]

    def get_most_recent_value(self):
        return self.get_values(1).value

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class SensorValue(UUIDModel):
    sensor = models.ForeignKey('sensors.Sensor',  on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now_add=True, blank=True)
    value = models.TextField()

    def __unicode__(self):
        return self.value

    def __str__(self):
        return self.value
