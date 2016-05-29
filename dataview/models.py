from django.contrib.gis.db import models
from django.conf import settings
from django.forms import ModelForm
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

import uuid
import hashlib
import os


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


class Node(UUIDModel):
    """
    Nodes represent external systems that dataview has knowledge of or manages
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Attribute(UUIDModel):
    node = models.ForeignKey(Node)
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    def set_value(self, value):
        self.value = value
        self.save()

    def get_value(self):
        return self.value

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


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


class X509Certificate(UUIDModel):
    cert = models.TextField(unique=True)
    file_name = models.CharField(max_length=255, unique=True)

    @staticmethod
    def get_base_path():
        return settings.BASE_DIR + '/certificates/'

    @staticmethod
    def create_from_str(certificate):
        if not os.path.exists(X509Certificate.get_base_path()):
            os.makedirs(X509Certificate.get_base_path())

        try:
            c = X509Certificate.objects.get(cert=certificate)
            # The certificate exists in the database, but not the filesystem
        except ObjectDoesNotExist:
            # The certificate does not exist in the database
            c = X509Certificate()
            c.cert = certificate
            c.file_name = hashlib.sha256(c.cert.encode('utf-8')).hexdigest() + '.pem'

        with open(X509Certificate.get_base_path() + c.file_name, 'w') as f:
            f.write(c.cert)

        try:
            c.save()
        except IntegrityError:
            pass

        return c

    def get_location(self):
        return X509Certificate.get_base_path() + self.file_name

    def get_file_from_str(certificate):
        path = X509Certificate.get_base_path() + X509Certificate.objects.get(cert=certificate).file_name

        with open(path, 'r'):
            pass

        return path


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
