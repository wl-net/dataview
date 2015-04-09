from django.db import models
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from building.models import Address
from dataview.common.models import UUIDModel

from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry

import datetime, requests, json

# general fields
WEEKDAYS = [
  (0, "Monday"),
  (1, "Tuesday"),
  (2, "Wednesday"),
  (3, "Thursday"),
  (4, "Friday"),
  (5, "Saturday"),
  (6, "Sunday"),
]

MESSAGE_TYPES = [
  (0, "sucess"),
  (1, "info"),
  (2, "warning"),
  (3, "danger"),
]

class ServiceType(UUIDModel):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Service(UUIDModel):
    name = models.CharField(max_length=128)
    service_type = models.ForeignKey('ServiceType')
    location = models.ForeignKey('building.Address')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Guest(UUIDModel):
    user = models.ForeignKey('auth.User', editable=False)

    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Event(UUIDModel):
    """
    Events are sourced either internally or externally
    """
    account = models.ForeignKey('dataview.Account')
    time = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    """
    types should be of the form app.namespace.your_event
    """
    type = models.CharField(max_length=60)

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return self.action

    def __str__(self):
        return self.action

class Message(UUIDModel):
    user = models.ForeignKey('auth.User', editable=False)
    time = models.DateTimeField()
    acknowledged = models.BooleanField(default=False)
    relevant = models.BooleanField(default=True)
    marked = models.DateTimeField()
    subject = models.CharField(max_length=128)
    message = models.TextField()
    type = models.IntegerField(choices=MESSAGE_TYPES)
    
    def acknowledge(self):
        self.acknowledged = True
        marked = datetime.datetime.now()

    def get_type(self):
        return str(MESSAGE_TYPES[self.type][1])

    def __unicode__(self):
        return self.subject
    
    def __str__(self):
        return self.subject
