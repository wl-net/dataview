from django.db import models
from django.core.validators import URLValidator
from portal.models import Room

class Light(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Room')
    description = models.TextField(blank=True)

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Speaker(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('portal.room')

    def set_volume(self, volume):
      self.volume = self.old_volume = volume

    def get_volume(self):
      return self.volume

    def mute(self):
      self.old_volume = self.volume
      self.volume = 0

    def unmute(self):
      self.volume = self.old_volume

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
