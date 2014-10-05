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
