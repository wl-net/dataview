from django.db import models
from django.contrib.gis.db import models
from portal.models import Address

class SystemDeployment(models.Model):
    name = models.CharField(max_length=128)
    hostname = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Address')
    is_master = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
