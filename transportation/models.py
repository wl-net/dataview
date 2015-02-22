from django.db import models

class TransportationInformationProvider(models.Model):
    name = models.CharField(max_length = 128)
    api_source = models.CharField(max_length=255)