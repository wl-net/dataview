from django.db import models
from dataview.common.models import UUIDModel

# Create your models here.
class Bank(UUIDModel):
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Budget(UUIDModel):
    name = models.CharField(max_length=128)
    description = models.TextField()

class Transaction(UUIDModel):
    uuid = models.CharField(max_length=36)
    transactionid = models.CharField(max_length=36)
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=60)
    recorded_total = models.IntegerField(default=0)
    location = models.ForeignKey('building.Address')
    memo = models.TextField()

    def __unicode__(self):
        return "$" + str(self.recorded_total) + " at " + self.name
    