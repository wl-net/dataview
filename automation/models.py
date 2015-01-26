from django.db import models
from django.forms import ModelForm
from django.core.validators import URLValidator
from portal.models import Room
from importlib import import_module
import sys, json

class Automator(models.Model):
    name = models.CharField(max_length=60)
    account = models.ForeignKey('dataview.Account')
    cls = models.CharField(max_length=128)
    description = models.TextField()
    configuration = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_instance(self):
        import_module(self.cls[:self.cls.rfind(".")])
        module = sys.modules[self.cls[:self.cls.rfind(".")]]
        clsName = getattr(module, self.cls[(self.cls.rfind(".")+1):len(self.cls)])
        return clsName(json.loads(self.configuration))

class Decider(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Controller(models.Model):
    name = models.CharField(max_length = 128)
    description = models.TextField()
    account = models.ForeignKey('dataview.Account')
    deciders = models.ManyToManyField('automation.Decider', through='ControllerDecider')
    automator = models.ForeignKey('automation.Automator')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class ControllerForm(ModelForm):
    class Meta:
        model = Controller
        fields = ['account']

class ControllerDecider(models.Model):
    notes = models.TextField()
    controller = models.ForeignKey(Controller)
    decider = models.ForeignKey(Decider)
    configuration = models.TextField()

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
    sources = models.ManyToManyField('automation.SpeakerSourceController')

    volume = 0

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

class SpeakerForm(ModelForm):
    class Meta:
        model = Speaker
        fields = ['name', 'location']

class SpeakerSourceController(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Residence')

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
