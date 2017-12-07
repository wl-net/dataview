from dataview.models import UUIDModel
from django.contrib.gis.db import models
import datetime, requests, json
from django.contrib.gis.geos import GEOSGeometry

class Address(UUIDModel):
    source_id = models.CharField(max_length=128, editable=False)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    geo = models.PointField(blank=True, null=True, srid=4326)

    def save(self, *args, **kwargs):
        try:
            request = requests.get("https://nominatim.openstreetmap.org/search?q=%s&format=json&polygon=1&addressdetails=0" % str(self).replace(' ', '%20'))
            response = json.loads(request.content.decode('utf-8'))
            self.geo = GEOSGeometry("POINT(" + response[0]['lon'] + " " + response[0]['lat'] + ")")
        except Exception as e:
            print(e)
=        super(Address, self).save(*args, **kwargs)

    def full_name(self):
        return self.street + " " + self.city + ", " + self.state + " " + self.zip

    def __unicode__(self):
        return self.street + " " + self.city + ", " + self.state + " " + self.zip

    def __str__(self):
        return self.street + " " + self.city + ", " + self.state + " " + self.zip

class Building(UUIDModel):
    address = models.ForeignKey(Address)
    name = models.CharField(max_length=128)

    YEAR_CHOICES = []
    for r in range(1900, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))
    built_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Room(UUIDModel):
    name = models.CharField(max_length=128)
    unit_number = models.CharField(max_length=8)
    location = models.ForeignKey(Building)
    square_feet = models.IntegerField()
    has_door = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name + " (" +  str(self.location) + ")"

    def __str__(self):
        return self.name + " (" +  str(self.location) + ")"

class Amenity(UUIDModel):
    location = models.ForeignKey(Building)
    name = models.CharField(max_length=128)
    reserverable = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
