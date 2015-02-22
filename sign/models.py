from django.db import models
from portal.models import Residence
from sign.sign_widgets import AbstractWidget

class Sign(models.Model):
    name = models.CharField(max_length=128)
    hostname = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Room')
    is_available = models.BooleanField(default=True)
    widgets = models.ManyToManyField('Widget', blank=True, null=True, through='SignWidget')
    background_image = models.ImageField(upload_to='sign/uploads/backgrounds', blank=True)

    def __unicode__(self):
        return self.name + " (" + self.location.name + ")"

    def __str__(self):
        return self.name + " (" + self.location.name + ")"

class Widget(models.Model):
    name = models.CharField(max_length=128)
    internal_name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @staticmethod
    def get_valid_cls_list():
        from django.conf import settings
        import os
        import glob2
        import importlib
        apps = []
        for app in settings.DATAVIEW_APPS:
            for file in glob2.glob(os.path.join(settings.BASE_DIR, '..', app, 'sign_widgets', "**/*.py")):
                path = file.replace(os.path.join(settings.BASE_DIR, '..') + '/', '', 1).replace('.py', '').replace('/', '.')

                mod = importlib.import_module(path)
                for member in dir(mod):
                    if isinstance(mod.__dict__[member], type) and issubclass(mod.__dict__[member], AbstractWidget) and member != 'AbstractWidget':
                        apps.append({'internal_name': member, 'path': path})
        return apps

    def update_widget_list(widgets=None):
        my_widgets = []
        for widget in Widget.objects.all():
            my_widgets.append({'internal_name': widget.name, 'path': widget.path})

        if widgets is None:
            widgets = Widget.get_valid_cls_list()
        for cls in widgets:
            if cls in my_widgets:
                my_widgets.remove(cls) # don't remove it
                widgets.remove(cls) # don't add it

        # add new widgets
        for cls in widgets:
            w = Widget()
            w.name = cls['internal_name']
            w.path = cls['path']

            w.save()

        # remove old widgets
        for old_cls in my_widgets:
            Widget.objects.filter(name=old_cls['internal_name']).filter(path = old_cls['path']).delete()

class SignWidget(models.Model):
    sign = models.ForeignKey(Sign)
    widget = models.ForeignKey(Widget)
    enabled = models.BooleanField(default=True)
    position = models.CharField(max_length=128)
    order = models.IntegerField()
    configuration = models.TextField()

    def __unicode__(self):
        return str(self.widget) + " on " + str(self.sign)

    def __str__(self):
        return str(self.widget) + " on " + str(self.sign)
