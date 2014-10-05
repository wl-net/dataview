from django.db import models
from portal.models import Residence

class Sign(models.Model):
    name = models.CharField(max_length=128)
    hostname = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Residence')
    is_available = models.BooleanField(default=True)