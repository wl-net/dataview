from django.db import models
from django.contrib.gis.db import models
from django.core.validators import URLValidator
import datetime

class Address(models.Model): 
    source_id = models.CharField(max_length=128, editable=False)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    #geo = models.GeometryField()
    
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
    rent = models.FloatField(default=0)
    floors = models.IntegerField(default=1)
    residence_floor = models.IntegerField(default=1)
    YEAR_CHOICES = []
    for r in range(1900, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))
    year = models.IntegerField(max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    active_building_community_number = models.IntegerField()
    active_building_community_website = models.TextField(blank=True,null=True)
    location = models.ForeignKey('Address')
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
        return name
    
    def __str__(self):
        return self.name

class Package(models.Model):
    tracking_number = models.CharField(max_length=128)
    location = models.ForeignKey('Residence')
    def __unicode__(self):
        return name
    
    def __str__(self):
        return self.name

# dataview models

class Message(models.Model):
    time = models.DateTimeField()
    location = models.ForeignKey('Residence')
    acknowledged = models.BooleanField(default=False)
    marked = models.DateTimeField()
    subject = models.CharField(max_length=128)
    message = models.TextField()
    
    def __unicode__(self):
        return self.subject
    
    def __str__(self):
        return self.subject

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
    
# Used for travel directions
class Destination(models.Model):
    title = models.CharField(max_length=128)    
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    #geo = models.GeometryField()
    def __unicode__(self):
        return title
    
    def __str__(self):
        return self.title