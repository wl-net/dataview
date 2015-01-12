from django.db import models

from portal.models import Address

class Camera(models.Model):
    location = models.CharField(max_length=128)
    residence = models.ForeignKey('portal.Residence')
    
    def __unicode__(self):
        return self.location

    def __str__(self):
        return self.location

class SafetyIncidentSource(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class SafetyIncidentAlert(models.Model):
    #user = models.User()
    incident = models.ForeignKey('security.SafetyIncident')
    location = models.ForeignKey('portal.address')

class SafetyIncident(models.Model):
    source = models.ForeignKey('security.SafetyIncidentSource')#, editable=False)
    location = models.CharField(max_length=128)
    time = models.DateTimeField()
    units = models.TextField(blank=True)
    type = models.CharField(max_length=128)

    class Meta:
        unique_together = ('location', 'time', 'units', 'type')
        get_latest_by = "time"

    def __unicode__(self):
        return self.type + '- ' + self.location

    def __str__(self):
        return self.type + '- ' + self.location
