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

class Transaction(models.Model):
    uuid = models.CharField(max_length=36)
    transactionid = models.CharField(max_length=36)
    uuid = models.CharField(max_length=36)
    uuid = models.CharField(max_length=36)
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=60)
    recorded_total = models.IntegerField(default=0)
    location = models.ForeignKey('Address')
    memo = models.TextField()

    def __unicode__(self):
        return "$" + str(self.recorded_total) + " at " + self.name
    
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
    year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    active_building_community_number = models.IntegerField()
    active_building_community_website = models.TextField(blank=True,null=True)
    rent = models.FloatField(default=0)
    tenants = models.ManyToManyField('auth.User', blank=True, null=True)

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

class Message(models.Model):
    user = models.ForeignKey('auth.User', editable=False)

    time = models.DateTimeField()
    location = models.ForeignKey('Residence')
    acknowledged = models.BooleanField(default=False)
    marked = models.DateTimeField()
    subject = models.CharField(max_length=128)
    message = models.TextField()
    type = models.IntegerField(choices=MESSAGE_TYPES)
    
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

# Used for travel directions
class Destination(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey('auth.User', editable=False)
    location = models.ForeignKey('Address')

    def is_open(self):
        #return datetime.datetime.today().time()
        if OpenHour.objects.filter(
            location=self.location, inverted=False, day_of_week=datetime.datetime.today().weekday(), from_time__lt=datetime.datetime.today().time(), to_time__gt=datetime.datetime.today().time()).count() == 1:
            return True
        else:
            for oh in OpenHour.objects.filter(location=self.location, inverted=True):
                if oh.to_time > datetime.datetime.today().time() and OpenHour.objects.filter(
                        location=self.location, inverted=True, day_of_week=max(0,datetime.datetime.today().weekday() - 1), from_time__gt=datetime.datetime.today().time(), to_time__lt=datetime.datetime.today().time()).count() == 1:
                    return True
                
                if oh.from_time < datetime.datetime.today().time():
                    return True
                
        return False
    
    def open_status(self):
        return "Open" if self.is_open() else "Closed"

    def __unicode__(self):
        return self.name + " (now " + self.open_status() + ")"
    
    def __str__(self):
        return self.name + " (now " + self.open_status() + ")"

class DestinationGroup(models.Model):
    name = models.CharField(max_length=60)
    destinations = models.ManyToManyField(Destination)

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class OpenHour(models.Model):
    location = models.ForeignKey('Address')
    day_of_week = models.IntegerField(choices=WEEKDAYS)
    from_time = models.TimeField()
    to_time = models.TimeField()
    inverted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.location) + " (" + str(self.from_time) + " - " + str(self.to_time) + ")"
    
    def __str__(self):
        return str(self.location) + " (" + str(self.from_time) + " - " + str(self.to_time) + ")"
    
    def save(self, *args, **kwargs):
        if self.to_time < self.from_time:
            self.inverted = True
        else:
            self.inverted = False
        super(OpenHour, self).save(*args, **kwargs)
    
    class Meta:
        unique_together = ("location", "day_of_week")
