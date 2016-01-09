import sys
import json

from django.db import models

from dataview.models import UUIDModel
from sign.sign_widgets import AbstractWidget
from importlib import import_module


class SignType(UUIDModel):
    name = models.CharField(max_length=128)
    internal_name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)

    @staticmethod
    def get_valid_cls_list():
        from django.conf import settings
        import os
        import glob2
        import importlib
        types = []
        for app in settings.DATAVIEW_APPS:
            for file in glob2.glob(os.path.join(settings.BASE_DIR, '..', app, 'sign_updaters', "**/*.py")):
                path = file.replace(os.path.join(settings.BASE_DIR, '..') + '/', '', 1).replace('.py', '').replace('/', '.')

                mod = importlib.import_module(path)
                for member in dir(mod):
                    try:
                        from sign.sign_updaters import AbstractSignUpdater
                        if isinstance(mod.__dict__[member], type) and issubclass(mod.__dict__[member], AbstractSignUpdater) and member != 'AbstractSignUpdater':
                            types.append({'name': mod.__dict__[member].SIGN_TYPE_NAME, 'internal_name': member, 'path': path.replace('.__init__','')})
                    except AttributeError as e:
                        print(e)
                        pass
        return types

    def get_instance(self, configuration):
        cls = self.path + '.' +  self.internal_name
        import_module(cls[:cls.rfind(".")])
        module = sys.modules[cls[:cls.rfind(".")]]
        clsName = getattr(module, cls[(cls.rfind(".")+1):len(cls)])
        return clsName(json.loads(configuration))

    def update_sign_type_list(sign_types=None):
        my_sign_types = []
        for sign_type in SignType.objects.all():
            my_sign_types.append({'name': sign_type.name, 'internal_name': sign_type.internal_name, 'path': sign_type.path})

        if sign_types is None:
            sign_types = SignType.get_valid_cls_list()

        common = []
        for cls in sign_types:
            if cls in my_sign_types:
                common.append(cls)

        for cls in common:
                my_sign_types.remove(cls) # don't remove it
                sign_types.remove(cls) # don't add it

        # add new sign_types
        for cls in sign_types:
            w = SignType()
            w.name = cls['name']
            w.internal_name = cls['internal_name']
            w.path = cls['path']

            w.save()

        # remove old sign_types
        for old_cls in my_sign_types:
            SignType.objects.filter(internal_name=old_cls['internal_name']).filter(path = old_cls['path']).delete()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Sign(UUIDModel):
    name = models.CharField(max_length=128)
    hostname = models.CharField(max_length=128)
    location = models.ForeignKey('building.Room', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    widgets = models.ManyToManyField('Widget', blank=True, through='SignWidget')
    background_image = models.ImageField(upload_to='sign/uploads/backgrounds', blank=True)
    backend_configuration = models.TextField(blank=True, default='{}')
    type = models.ForeignKey(SignType)

    @staticmethod
    def update_signs():
        sws = SignWidget.objects.all()
        for sw in sws:
            updater = sw.sign.type.get_instance(sw.sign.backend_configuration)
            updater.update_widget(sw)

    def reload_sign(self):
        updater = self.type.get_instance(self.backend_configuration)
        updater.reload_signs(str(self.id))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Widget(UUIDModel):
    name = models.CharField(max_length=128)
    internal_name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    external_id = models.CharField(max_length=60)

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
                    except AttributeError as e:
                        print(e)
                        pass
        return widgets

    def get_instance(self, configuration):
        cls = self.path + '.' +  self.internal_name
        import_module(cls[:cls.rfind(".")])
        module = sys.modules[cls[:cls.rfind(".")]]
        class_name = getattr(module, cls[(cls.rfind(".")+1):len(cls)])
        return class_name(json.loads(configuration))

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


class SignWidget(UUIDModel):
    sign = models.ForeignKey(Sign)
    widget = models.ForeignKey(Widget)
    enabled = models.BooleanField(default=True)
    backend_configuration = models.TextField(default='{}')
    frontend_configuration = models.TextField(default='{}')

    def __unicode__(self):
        return str(self.widget) + " on " + str(self.sign)

    def __str__(self):
        return str(self.widget) + " on " + str(self.sign)
