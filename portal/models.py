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

# ActiveBuilding Models

class Residence(UUIDModel):
    name = models.CharField(max_length=64)
    location = models.ForeignKey('building.Address')
    floors = models.IntegerField(default=1)
    residence_floor = models.IntegerField(default=1)
    YEAR_CHOICES = []
    for r in range(1900, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    rent = models.FloatField(default=0)
    tenants = models.ManyToManyField('auth.User', blank=True)

    def __unicode__(self):
        return self.name + " " + self.location.city

    def __str__(self):
        return self.name + " " + self.location.city 

class Package(UUIDModel):
    tracking_number = models.CharField(max_length=128)
    location = models.ForeignKey('Residence')
    picked_up = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Neighbor(UUIDModel):
    user = models.ForeignKey('auth.User', editable=False)

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    location = models.ForeignKey('Residence')
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name
# dataview models

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
    location = models.ForeignKey('Residence')
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
