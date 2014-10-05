from django.db import models
from portal.models import Residence

class Sign(models.Model):
    name = models.CharField(max_length=128)
    hostname = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Room')
    is_available = models.BooleanField(default=True)
    widgets = models.ManyToManyField('Widget', blank=True, null=True)

    def __unicode__(self):
        return self.name + " (" + self.location.name + ")"

    def __str__(self):
        return self.name + " (" + self.location.name + ")"

class Widget(models.Model):
    name = models.CharField(max_length=128)
    internal_name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class SignWidgetConfig(models.Model):
    sign = models.ForeignKey('Sign')
    widget = models.ForeignKey('Widget')
