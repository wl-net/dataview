from django.db import models

# Create your models here.

class Budget(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
