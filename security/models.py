from django.db import models

class Camera(models.Model):
    location = models.CharField(max_length=128)
    residence = models.ForeignKey('portal.Residence')
    
    def __unicode__(self):
        return self.location

    def __str__(self):
        return self.location
