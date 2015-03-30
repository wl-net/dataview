from django.db import models
from portal.models import Residence
from sign.sign_widgets import AbstractWidget
from importlib import import_module
import sys, json

class Sign(models.Model):
    name = models.CharField(max_length=128)
    hostname = models.CharField(max_length=128)
    location = models.ForeignKey('portal.Room')
    is_available = models.BooleanField(default=True)
    widgets = models.ManyToManyField('Widget', blank=True, null=True, through='SignWidget')
    background_image = models.ImageField(upload_to='sign/uploads/backgrounds', blank=True)


    def update_signs():
        sws = SignWidgets.objects.all()
        for sw in sws:
            wi = sw.widget.get_instance(sw.configuration)
            contents = wi.get_contents()

            # dashing specific code

        pass

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
        widgets = []
        for app in settings.DATAVIEW_APPS:
            for file in glob2.glob(os.path.join(settings.BASE_DIR, '..', app, 'sign_widgets', "**/*.py")):
                path = file.replace(os.path.join(settings.BASE_DIR, '..') + '/', '', 1).replace('.py', '').replace('/', '.')

                mod = importlib.import_module(path)
                for member in dir(mod):
                    try:
                        if isinstance(mod.__dict__[member], type) and issubclass(mod.__dict__[member], AbstractWidget) and member != 'AbstractWidget':
                            widgets.append({'name': mod.__dict__[member].WIDGET_NAME, 'internal_name': member, 'path': path.replace('.__init__','')})
                    except AttributeError:
                        pass
        return widgets

    def get_instance(self, configuration):
        cls = self.path + '.' +  self.internal_name
        import_module(cls[:cls.rfind(".")])
        module = sys.modules[cls[:cls.rfind(".")]]
        clsName = getattr(module, cls[(cls.rfind(".")+1):len(cls)])
        return clsName(json.loads(configuration))

    def update_widget_list(widgets=None):
        my_widgets = []
        for widget in Widget.objects.all():
            my_widgets.append({'name': widget.name, 'internal_name': widget.internal_name, 'path': widget.path})

        if widgets is None:
            widgets = Widget.get_valid_cls_list()

        common = []
        for cls in widgets:
            if cls in my_widgets:
                common.append(cls)

        for cls in common:
                my_widgets.remove(cls) # don't remove it
                widgets.remove(cls) # don't add it

        # add new widgets
        for cls in widgets:
            w = Widget()
            w.name = cls['name']
            w.internal_name = cls['internal_name']
            w.path = cls['path']

            w.save()

        # remove old widgets
        for old_cls in my_widgets:
            Widget.objects.filter(internal_name=old_cls['internal_name']).filter(path = old_cls['path']).delete()

class SignWidget(models.Model):
    sign = models.ForeignKey(Sign)
    widget = models.ForeignKey(Widget)
    enabled = models.BooleanField(default=True)
    position = models.CharField(max_length=128)
    order = models.IntegerField()
    backend_configuration = models.TextField(default='{}')
    frontend_configuration = models.TextField(default='{}')

    def __unicode__(self):
        return str(self.widget) + " on " + str(self.sign)

    def __str__(self):
        return str(self.widget) + " on " + str(self.sign)
