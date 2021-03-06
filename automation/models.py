from django.db import models
from django.forms import ModelForm
from importlib import import_module

import sys, json

from automation.automators import AbstractAutomator
from automation.deciders import AbstractDecider
from dataview.models import Event, UUIDModel, Node


class Automator(UUIDModel):
    name = models.CharField(max_length=60,
                            help_text="Give your automator a name. For example: " +
                                      "<strong>Downtown Seattle: Kitchen Automatic Blinds</strong>")
    account = models.ForeignKey('dataview.Account', on_delete=models.CASCADE)
    backend = models.ForeignKey('automation.AutomatorClass',
                                help_text="This backend will be responsible for performing the actions you desire. "
                                          "Your Dataview administrator can provision additional backends for you to use.",
                                on_delete=models.CASCADE)
    description = models.TextField(blank=True, help_text="What does this Automator do?")
    configuration = models.TextField( default='{}', help_text="Don't modify this unless you know understand how the " +
                                                           "automator processes configuration")
    nodes = models.ManyToManyField(Node, blank=True,
                                   help_text="These nodes will be associated with this automator and "
                                             "granted access to any credentials")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_attributes(self):
        """
        Get exported attributes
        :return:
        """
        return self.get_instance().get_attributes()

    def save(self, *args, **kwargs):
        # self.configuration = json.dumps(self.get_class().populate_configuration(json.loads(self.configuration)))
        super(Automator, self).save(*args, **kwargs)

    def get_class(self):
        cls = self.backend.path + '.' +  self.backend.name
        import_module(cls[:cls.rfind(".")])
        module = sys.modules[cls[:cls.rfind(".")]]
        return getattr(module, cls[(cls.rfind(".")+1):len(cls)])

    def get_instance(self):
        return self.get_class()(json.loads(self.configuration))

    def do_operations(self, operations, instance=None, logging=True, duplicate=False):
        i = self.get_instance()
        response = []
        for operation in json.loads(operations):
            success = True
            try:
                response.append(getattr(i, operation["method"])(*operation["params"]))
            except Exception as e:
                success = False
                response.append(e)

            if logging:
                e = Event()
                e.account = self.account
                e.action = self.name + ': ' + operation['method']
                if operation['method']:
                    e.action = e.action + ' ' + ' '.join(operation['params'])
                e.type = 'automation.operation'

                details = operation.copy()
                details.update({'name': self.name, 'success': success})
                e.detail = json.dumps(details)

                e.save()

        return response

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


class AutomatorClass(UUIDModel):
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

        classes_to_create = []
        for cls in classes:
            if cls not in my_classes:
                classes_to_create.append(cls)
            else:
                my_classes.remove(cls)

        # add new classes
        for cls in classes_to_create:
            ac = AutomatorClass()
            ac.name = cls['name']
            ac.path = cls['path']

            ac.save()

        # remove old classes
        for old_cls in my_classes:
            AutomatorClass.objects.filter(name=old_cls['name']).filter(path=old_cls['path']).delete()


class AutomatorForm(ModelForm):
    class Meta:
        model = Automator
        fields = ['name', 'account', 'backend', 'description', 'configuration', 'nodes']


class Action(UUIDModel):
    automator = models.ForeignKey(Automator, on_delete=models.CASCADE)
    method = models.CharField(max_length=128)
    operations = models.TextField()
    time = models.DateTimeField(auto_now=True)


class Task(UUIDModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    operations = models.TextField(default='[]')
    automator = models.ForeignKey(Automator, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def do_operations(self, placeholders={}):
        prepared_operations = json.loads(self.operations)
        for operation in prepared_operations:

            params = operation.get('params')
            operation.update({'params': [str(param) .format(**placeholders) for param in params]})

        return self.automator.do_operations(json.dumps(prepared_operations))


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'automator', 'operations']


class TaskGroup(UUIDModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    tasks = models.ManyToManyField(Task)
    is_task_wrapper = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def do_operations(self, placeholders={}):
        for task in self.tasks.all():
            task.automator.do_operations(task.operations)


class Decider(UUIDModel):
    """
    Think of deciders as a machine that answers with "Yes" or "No" depsite
    possibly complicated (configurable) conditions to reach that decision.
    For example: Is it warm outside?
    """
    name = models.CharField(max_length=128, help_text="Give your decider a name. For example: <strong>Am I sleeping?</strong>")
    description = models.TextField(blank=True)
    conditions = models.TextField(blank=True, help_text="This is the set of rules the decider uses to make its decision.", default='{}')
    configuration = models.TextField(blank=True, help_text="Optional configuration", default='{}')
    backend = models.ForeignKey('automation.DeciderClass', on_delete=models.CASCADE,
                                help_text="This backend will be responsible for making decisions. Your Dataview administrator can provision additional internal backends for you to use.")

    @staticmethod
    def get_valid_cls_list():
        from django.conf import settings
        import os
        import glob2
        import importlib
        apps = []
        for app in settings.DATAVIEW_APPS:
            for file in glob2.glob(os.path.join(settings.BASE_DIR, '..', app, 'deciders', "**/*.py")):
                path = file.replace(os.path.join(settings.BASE_DIR, '..') + '/', '', 1).replace('.py', '').replace('/', '.')

                mod = importlib.import_module(path)
                for member in dir(mod):
                    if isinstance(mod.__dict__[member], type) and issubclass(mod.__dict__[member], AbstractDecider) and member != 'AbstractDecider':
                        apps.append({'name': member, 'path': path})
        return apps

    def get_instance(self):
        cls = self.backend.path + '.' + self.backend.name
        import_module(cls[:cls.rfind(".")])
        module = sys.modules[cls[:cls.rfind(".")]]
        name = getattr(module, cls[(cls.rfind(".")+1):len(cls)])
        try:
            config = json.loads(self.configuration)
        except IOError:
            config = {}

        return name(json.loads(self.conditions), config)

    def decide(self):
        i = self.get_instance()
        return {'boolean': i.decide(), 'numeric': i.fuzzy_decide(), 'string_descriptive': i.get_decision_reason()}

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class DeciderClass(UUIDModel):
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
        for cls in DeciderClass.objects.all():
            my_classes.append({'name': cls.name, 'path': cls.path})

        if classes is None:
            classes = Decider.get_valid_cls_list()

        classes_to_create = []
        for cls in classes:
            if cls not in my_classes:
                classes_to_create.append(cls)
            else:
                my_classes.remove(cls)

        # add new classes
        for cls in classes_to_create:
            ac = DeciderClass()
            ac.name = cls['name']
            ac.path = cls['path']

            ac.save()

        # remove old classes
        #for old_cls in my_classes:
        #    DeciderClass.objects.filter(name=old_cls['name']).filter(path=old_cls['path']).delete()


class DeciderForm(ModelForm):
    class Meta:
        model = Decider
        fields = ['name', 'backend', 'description', 'conditions', 'configuration']


class Controller(UUIDModel):
    name = models.CharField(max_length=128,
                            help_text="Give your controller a name. For example a controller that " +
                                      "turns off lights when you go to sleep might be called <strong>Sleep Conditions</strong>")
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    deciders = models.ManyToManyField('automation.Decider', through='ControllerDecider',
                                      help_text="Specify the deciders you are interested in using. You'll configure them later")
    tasks = models.ManyToManyField('automation.Task', through='ControllerTask')
    configuration = models.TextField(default='{}')
    state = models.TextField(default={})

    def decide(self):
        decisions = {}
        result = True
        for decider in self.deciders.all():
            decisions[decider.name] = decider.decide()

        for decision in decisions:
            if not decisions[decision]['boolean']:
                result = False

        return {'result': result, 'decisions': decisions}

    def automate(self):
        if not self.enabled:
            return

        decision = self.decide()

        config = json.loads(self.configuration)
        dualmode = 'restore_state' in config and config['restore_state']
        dualmode_run = False

        decision = decision['result']
        if dualmode:
            state = json.loads(self.state)
            if 'last_decision' not in state or state['last_decision'] != str(decision):
                dualmode_run = True
                state['last_decision'] = str(decision)
                self.state = json.dumps(state)
                self.save()

        if decision or dualmode_run:
            for ct in ControllerTask.objects.filter(controller=self):
                ct_config = json.loads(ct.mapping)
                if dualmode:
                    if ('dualmode' in ct_config and
                                ct_config['dualmode'] != decision):
                        continue
                    if 'dualmode' not in ct_config and not decision:
                        continue
                    if not dualmode_run:
                        continue
                ct.task.do_operations()

    def is_complete(self):
        return self.tasks.all().count() > 0 and self.deciders.all().count()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class ControllerForm(ModelForm):
    class Meta:
        model = Controller
        fields = ['name', 'enabled', 'description']
    # ManyToManyFields that can't be handled automatically
    #automators = ModelMultipleChoiceField(queryset=Automator.objects.all())
    #deciders = ModelMultipleChoiceField(queryset=Decider.objects.all())


class ControllerDecider(UUIDModel):
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    decider = models.ForeignKey(Decider, on_delete=models.CASCADE)


class ControllerDeciderForm(ModelForm):
    class Meta:
        model = ControllerDecider
        fields = ['controller', 'decider']


class ControllerTask(UUIDModel):
    notes = models.TextField()
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    mapping = models.TextField()

    def perform_operations(self, provided_decisions):
        ops = json.loads(self.mapping)
        #for descisionblock in ops:
            #for decision in descisionblock:
            #    if decision not in provided_decisions:
            #a = Automator.objects.get(automator)
            #a.get_instance()
            #a.perform_operations(operations)


class ControllerTaskForm(ModelForm):
    class Meta:
        model = ControllerTask
        fields = ['notes', 'task', 'mapping']
