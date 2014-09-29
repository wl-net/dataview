from django.db import models
from django.core.validators import URLValidator

class Light(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Mood(models.Model):
    title = models.CharField(max_length=128)
    enabled = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return title
    
    def __str__(self):
        return self.title
    
class RadioStation(models.Model):
    name = models.CharField(max_length=128)
    url = models.TextField(validators=[URLValidator()], unique=True)
    mood = models.ManyToManyField(Mood, blank=True, null=True)

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name