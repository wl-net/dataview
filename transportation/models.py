from django.db import models
from dataview.common.models import UUIDModel
from portal.models import Address

WEEKDAYS = [
  (0, "Monday"),
  (1, "Tuesday"),
  (2, "Wednesday"),
  (3, "Thursday"),
  (4, "Friday"),
  (5, "Saturday"),
  (6, "Sunday"),
]

class TransportationInformationProvider(UUIDModel):
    name = models.CharField(max_length = 128)
    api_source = models.CharField(max_length=255)

# Used for travel directions
class Destination(UUIDModel):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Address')

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

class DestinationGroup(UUIDModel):
    name = models.CharField(max_length=60)
    destinations = models.ManyToManyField(Destination)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class OpenHour(UUIDModel):
    location = models.ForeignKey('portal.Address')
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
