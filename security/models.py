from django.contrib.gis.db import models
from dataview.models import UUIDModel
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models import MultiPolygonField
from django.db.models import Manager as GeoManager

import requests
import json
import re


class Camera(UUIDModel):
    location = models.CharField(max_length=128)
    residence = models.ForeignKey('building.Building', on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.location

    def __str__(self):
        return self.location


class SecuritySystem(UUIDModel):
    name = models.CharField(max_length=128)
    residence = models.ForeignKey('residential.Residence', on_delete=models.CASCADE)
    configuration = models.TextField(default='{}')
    lock_taskgroup = models.ForeignKey('automation.TaskGroup', related_name='lock_taskgroup', on_delete=models.CASCADE)
    unlock_taskgroup = models.ForeignKey('automation.TaskGroup', related_name='unlock_taskgroup', on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class AuthenticationFactor(UUIDModel):
    name = models.CharField(max_length=128)
    security_system = models.ManyToManyField('security.SecuritySystem')
    configuration = models.TextField(default='{}')

    def __unicode__(self):
        return self.name

    def __str__(self):
         return self.name


class SafetyIncidentSource(UUIDModel):
    name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class SafetyIncidentAlert(UUIDModel):
    incident = models.ForeignKey('security.SafetyIncident', on_delete=models.CASCADE)
    boundary = models.ForeignKey('security.SafetyIncidentAlertBoundary', on_delete=models.CASCADE)
    escalated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("incident", "boundary")


class SafetyIncidentAlertBoundary(UUIDModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    geobox = MultiPolygonField()
    enabled = models.BooleanField(default=True)
    objects = GeoManager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class SafetyIncident(UUIDModel):
    source = models.ForeignKey('security.SafetyIncidentSource', editable=False, on_delete=models.CASCADE)
    location = models.CharField(max_length=128)
    time = models.DateTimeField()
    units = models.TextField(blank=True)
    type = models.CharField(max_length=128)
    geo = models.PointField(blank=True, null=True, srid=3857)

    class Meta:
        unique_together = ('location', 'time', 'units', 'type')
        get_latest_by = "time"

    def get_address(self):
        pass

    def save(self, *args, **kwargs):
        try:
            request = requests.get('https://nominatim.openstreetmap.org/search?q={} Seattle&format=json&polygon=1&addressdetails=0'.format(
                re.sub('%20St$', '', str(self.location).replace('/', 'and').replace(' ', '%20'))))
            response = json.loads(request.content.decode('utf-8'))
            self.geo = GEOSGeometry('POINT({} {})'.format(response[0]['lon'], response[0]['lat']))

        except Exception as e:
            pass

        super(SafetyIncident, self).save(*args, **kwargs)

        if self.geo:
            for sab in SafetyIncidentAlertBoundary.objects.filter(enabled=True):
                if sab.geobox.contains(self.geo):
                    sia = SafetyIncidentAlert()
                    sia.boundary = sab
                    sia.incident = self
                    sia.save()

    def __unicode__(self):
        return self.type + '- ' + self.location

    def __str__(self):
        return self.type + '- ' + self.location + str(self.geo)
