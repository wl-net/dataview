from django.db import models
from dataview.models import UUIDModel
from building.models import Address, Building

class Camera(UUIDModel):
    location = models.CharField(max_length=128)
    residence = models.ForeignKey('building.Building')
    
    def __unicode__(self):
        return self.location

    def __str__(self):
        return self.location

class SafetyIncidentSource(UUIDModel):
    name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class SafetyIncidentAlert(UUIDModel):
    incident = models.ForeignKey('security.SafetyIncident')
    location = models.ForeignKey('building.address')

from django.contrib.gis.db.models import MultiPolygonField

class SafetyIncidentAlertBoundary(UUIDModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    geobox = MultiPolygonField()
    enabled = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class SafetyIncident(UUIDModel):
    source = models.ForeignKey('security.SafetyIncidentSource', editable=False)
    location = models.CharField(max_length=128)
    time = models.DateTimeField()
    units = models.TextField(blank=True)
    type = models.CharField(max_length=128)

    class Meta:
        unique_together = ('location', 'time', 'units', 'type')
        get_latest_by = "time"

    def get_address(self):
        pass
    #def save(self, *args, **kwargs):
    #    super(SafetyIncident, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.type + '- ' + self.location

    def __str__(self):
        return self.type + '- ' + self.location
