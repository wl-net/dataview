from django.db import models
from django.contrib.gis.db import models
from portal.models import Address


class SystemDeployment(models.Model):
    """ System Deployments represent a server that hosts Dataview."""

    """ the name of the dataview deployment. Whatever you want"""
    name = models.CharField(max_length=128)

    """ the FQDN that can be used to manage this specific dataview deployment"""
    hostname = models.CharField(max_length=128)

    """ the physical location of the dataview server"""
    location = models.ForeignKey('portal.Address')

    is_master = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
