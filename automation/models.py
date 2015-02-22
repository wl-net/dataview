from django.db import models
from django.forms import ModelForm, ModelMultipleChoiceField
from django.core.validators import URLValidator
from portal.models import Room
from importlib import import_module
import sys, json
from automation.automators import AbstractAutomator

class Automator(models.Model):
    name = models.CharField(max_length=60)
    account = models.ForeignKey('dataview.Account')
    backend = models.ForeignKey('automation.AutomatorClass')
    description = models.TextField()
    configuration = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_instance(self):
        cls = self.backend.path + '.' +  self.backend.name 
        import_module(cls[:cls.rfind(".")])
        module = sys.modules[cls[:cls.rfind(".")]]
        clsName = getattr(module, cls[(cls.rfind(".")+1):len(cls)])
        return clsName(json.loads(self.configuration))

    def do_operations(self, operations, instance=None):
        i = self.get_instance()
        for operation in json.loads(operations):
            getattr(i, operation["method"])(*operation["params"])

    @staticmethod
    def get_valid_cls_list():
        from django.conf import settings
        import os
        import glob2
        import importlib
        apps = []
        for app in settings.DATAVIEW_APPS:
            for file in glob2.glob(os.path.join(settings.BASE_DIR, '..', app, 'automators', "**/*.py")):
                path = file.replace(os.path.join(settings.BASE_DIR, '..') + '/', '', 1).replace('.py', '').replace('/', '.')

                mod = importlib.import_module(path)
                for member in dir(mod):
                    if isinstance(mod.__dict__[member], type) and issubclass(mod.__dict__[member], AbstractAutomator) and member != 'AbstractAutomator':
                        apps.append({'name': member, 'path': path})
        return apps

class AutomatorClass(models.Model):
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)

    def __unicode__(self):
        return self.path + '.' + self.name

    def __str__(self):
        return self.path + '.' + self.name

    class Meta:
        unique_together = ('name', 'path',)

    def update_classes(classes=None):
        my_classes = []
        for cls in AutomatorClass.objects.all():
            my_classes.append({'name': cls.name, 'path': cls.path})

        if classes is None:
            classes = Automator.get_valid_cls_list()
        for cls in classes:
            if cls in my_classes:
                my_classes.remove(cls) # don't remove it
                classes.remove(cls) # don't add it

        # add new classes
        for cls in classes:
            ac = AutomatorClass()
            ac.name = cls['name']
            ac.path = cls['path']

            ac.save()

        # remove old classes
        for old_cls in my_classes:
            AutomatorClass.objects.filter(name=old_cls['name']).filter(path = old_cls['path']).delete()

class Decider(models.Model):
    """
    Think of deciders as a machine that answers with "Yes" or "No" depsite
    possibly complicated (configurable) conditions to reach that decision.
    For example: Is it warm outside?
    """
    name = models.CharField(max_length=128)
    description = models.TextField()
    configuration = models.TextField()

    def decide(self):
        return False

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Controller(models.Model):
    name = models.CharField(max_length = 128)
    description = models.TextField()
    deciders = models.ManyToManyField('automation.Decider', through='ControllerDecider')
    automator = models.ManyToManyField('automation.Automator', through='ControllerAutomator')

    def decide(self):
        for decider in self.deciders.all():
            decider.decide()

    def automate(self):
        decision = self.decide()
        for automator in self.automator.all():
            ca = ControllerAutomator.get(automator=automator, controller=controller)
            config = json.loads(ca.operations)
            ops = ca['decision']['binary'][decision]
            for op in ops:
              automator.do_operations()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class ControllerForm(ModelForm):
    class Meta:
        model = Controller
        fields = ['name', 'description']
    # ManyToManyFields that can't be handled automatically
    automators = ModelMultipleChoiceField(queryset=Automator.objects.all())
    deciders = ModelMultipleChoiceField(queryset=Decider.objects.all())

class ControllerDecider(models.Model):
    controller = models.ForeignKey(Controller)
    decider = models.ForeignKey(Decider)

class ControllerAutomator(models.Model):
    notes = models.TextField()
    controller = models.ForeignKey(Controller)
    automator = models.ForeignKey(Automator)
    operations = models.TextField()

    def perform_operations(self):
        ops = json.loads(self.operations)

class Light(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Room')
    description = models.TextField(blank=True)

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Speaker(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('portal.room')
    sources = models.ManyToManyField('automation.SpeakerSourceController')

    volume = 0

    def set_volume(self, volume):
      self.volume = self.old_volume = volume

    def get_volume(self):
      return self.volume

    def mute(self):
      self.old_volume = self.volume
      self.volume = 0

    def unmute(self):
      self.volume = self.old_volume

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class SpeakerForm(ModelForm):
    class Meta:
        model = Speaker
        fields = ['name', 'location']

class SpeakerSourceController(models.Model):
    name = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Residence')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Mood(models.Model):
    title = models.CharField(max_length=128)
    enabled = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return title

    def __str__(self):
        return self.title

class RadioStation(models.Model):
    name = models.CharField(max_length=128)
    url = models.TextField(validators=[URLValidator()], unique=True)
    mood = models.ManyToManyField(Mood, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
