from django.db import models

class Camera(models.Model):
    location = models.CharField(max_length=128)
    residence = models.ForeignKey('portal.Residence')
    
    def __unicode__(self):
        return self.location

    def __str__(self):
        return self.location

class SafetyIncident(models.Model):
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
