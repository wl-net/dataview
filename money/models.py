from django.db import models

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Budget(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

class Transaction(models.Model):
    uuid = models.CharField(max_length=36)
    transactionid = models.CharField(max_length=36)
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=60)
    recorded_total = models.IntegerField(default=0)
    location = models.ForeignKey('portal.Address')
    memo = models.TextField()

    def __unicode__(self):
        return "$" + str(self.recorded_total) + " at " + self.name
    