from django.db import models
from django.core.validators import URLValidator
from django.contrib.auth.models import User

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

#class Application(models.Model):
#    name = models.CharField(max_length=128)

class Address(models.Model): 
    source_id = models.CharField(max_length=128, editable=False)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    geo = models.PointField(blank=True, null=True)

    def save(self, *args, **kwargs):
        request = requests.get("https://nominatim.openstreetmap.org/search?q=%s&format=json&polygon=1&addressdetails=0" % str(self).replace(' ', '%20'))
        response = json.loads(request.content.decode('utf-8'))
        self.geo = GEOSGeometry("POINT(" + response[0]['lat'] + " "+ response[0]['lon'] + ")")
        super(Address, self).save(*args, **kwargs)

    def full_name(self):
        return self.street + " " + self.city + ", " + self.state + " " + self.zip

    def __unicode__(self):
        return self.street + " " + self.city + ", " + self.state + " " + self.zip

    def __str__(self):
        return self.street + " " + self.city + ", " + self.state + " " + self.zip

class Location(models.Model):
    title = models.CharField(max_length=128)

# ActiveBuilding Models

class Residence(models.Model):
    name = models.CharField(max_length=64)
    location = models.ForeignKey('Address')
    floors = models.IntegerField(default=1)
    residence_floor = models.IntegerField(default=1)
    YEAR_CHOICES = []
    for r in range(1900, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    active_building_community_number = models.IntegerField()
    active_building_community_website = models.TextField(blank=True,null=True)
    rent = models.FloatField(default=0)
    tenants = models.ManyToManyField('auth.User', blank=True)

    def __unicode__(self):
        return self.name + " " + self.location.city

    def __str__(self):
        return self.name + " " + self.location.city 

class Amenity(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('Residence')
    reserverable = models.BooleanField(default=False)
    externalId = models.CharField(max_length=5)
    show = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Package(models.Model):
    tracking_number = models.CharField(max_length=128)
    location = models.ForeignKey('Residence')
    picked_up = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Neighbor(models.Model):
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

class Room(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('Residence')
    square_feet = models.IntegerField()
    has_door = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name + " (" +  str(self.location) + ")"

    def __str__(self):
        return self.name + " (" +  str(self.location) + ")"

class Employer(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('Address')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=128)
    service_type = models.ForeignKey('ServiceType')
    location = models.ForeignKey('Address')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Guest(models.Model):
    user = models.ForeignKey('auth.User', editable=False)

    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Event(models.Model):
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

class Message(models.Model):
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

class TimeEntry(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Time entries"

    def __unicode__(self):
        return str(self.start) + " - " +  str(self.end) + ", " + str(self.end - self.start)

    def __str__(self):
        return str(self.start) + " - " +  str(self.end) + ", " + str(self.end - self.start)
