from django.contrib.gis.db import models
from django.conf import settings
from django.forms import ModelForm, ModelMultipleChoiceField
import uuid

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class SystemDeployment(UUIDModel):
    """ System Deployments represent a server that hosts Dataview."""

    """ the name of the dataview deployment. Whatever you want"""
    name = models.CharField(max_length=128)

    """ the FQDN that can be used to manage this specific dataview deployment"""
    hostname = models.CharField(max_length=128)

    is_master = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)


class SystemDeploymentForm(ModelForm):
    class Meta:
        model = SystemDeployment
        fields = ['name', 'hostname']

class Account(UUIDModel):
    """ Accounts represent a collection of dataview users that rely on shared residences"""
    name = models.CharField(max_length=60, help_text="This will be displayed to all users you share your account with")
    users = models.ManyToManyField('auth.User', help_text="")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'users']

import hashlib
class X509Certificate(UUIDModel):
    cert = models.TextField(unique=True)
    file_name = models.CharField(max_length=255, unique=True)

    def create_from_str(certificate):
        c = X509Certificate()
        c.cert = certificate

        settings.BASE_DIR
        c.file_name = hashlib.sha256(c.cert.encode('utf-8')).hexdigest() + '.pem'
        f = open(settings.BASE_DIR + '/certificates/' + c.file_name, 'w')
        f.write(c.cert)
        f.close()

        c.save()

        return c

    def get_file_from_str(certificate):
        return settings.BASE_DIR + '/certificates/' + X509Certificate.objects.get(cert=certificate).file_name

class Event(UUIDModel):
    """
    Events are sourced either internally or externally
    """
    account = models.ForeignKey(Account)
    time = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    detail = models.TextField(blank=True)
    """
    types should be of the form app.namespace.your_event
    """
    type = models.CharField(max_length=60)

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return self.action

    def __str__(self):
        return self.action
