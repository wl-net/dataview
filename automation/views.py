from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from dataview.models import Event
from dataview.models import Account
from automation.models import Automator, AutomatorClass, Controller, Decider, TaskForm, AutomatorForm, ControllerForm
from automation.models import ControllerTask, ControllerTaskForm
from automation.models import ControllerDecider, DeciderForm, Task, TaskGroup

from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from guardian.shortcuts import get_objects_for_user

import json


def index(request):
    automators = get_objects_for_user(request.user, 'automation.change_automator')
    controllers = get_objects_for_user(request.user, 'automation.change_controller')
    deciders = get_objects_for_user(request.user, 'automation.change_decider')
    taskgroups = get_objects_for_user(request.user, 'automation.change_taskgroup')
    tasks = get_objects_for_user(request.user, 'automation.change_task').order_by('name')
    events = get_objects_for_user(request.user, 'dataview.change_event').filter(type='automation.operation')[:5]
    return render(request, 'automation/index.html', {'automators': automators,
                                                       'controllers': controllers, 'deciders': deciders,
                                                       'taskgroups': taskgroups, 'tasks': tasks, 'events': events})


class AutomateWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/portal/automation/')


def automators(request):
    automators = get_objects_for_user(request.user, 'automation.change_automator')
    return render(request, 'automation/automators.html', {'automators': automators})


def add_automator(request):
    if request.method == 'POST':
        form = AutomatorForm(request.POST, initial={'account': Account.objects.get(users=request.user)})
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automation-automators'))
    else:
        form = AutomatorForm(initial={'account': Account.objects.get(users=request.user)})
    return render(request, 'automation/add-automator.html', {'form': form})


def get_automator_default_config(request):
    a = AutomatorClass.objects.get(id=request.id)
    a.get_instance()


def edit_automator(request, automator):
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            get_objects_for_user(request.user, 'automation.change_automator').get(id=automator).delete()
            return HttpResponseRedirect(reverse('automation-automators'))

        form = AutomatorForm(request.POST, instance=get_objects_for_user(request.user, 'automation.change_automator').get(id=automator))
        if form.is_valid():
            form.save()
    else:
        form = AutomatorForm(instance = get_objects_for_user(request.user, 'automation.change_automator').get(id=automator))
        return render(request, 'automation/edit-automator.html', {'form': form})

    return render(request, 'automation/edit-automator.html', {'form': form})


def run_task(request):
    if request.method == 'POST':
        try:
            get_objects_for_user(request.user, 'automation.change_taskgroup').get(
                id=request.POST.get('task')).do_operations()
        except ObjectDoesNotExist:
            get_objects_for_user(request.user, 'automation.change_task').get(id=request.POST.get('task')).do_operations(
                json.loads(request.POST.get('params', default='{}')))

    # TODO: make this an API with proper response code.
    return HttpResponseRedirect(reverse('automation-index'))


def activity(request):
    events = Event.objects.filter(type='automation.operation')[:50]

    return render(request, 'automation/activity.html', {'events': events})


def edit_controllertask(request, controller, task):
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            get_objects_for_user(request.user, 'automation.change_controllertask').get(id=task).delete()
            return HttpResponseRedirect(reverse('automation-automators'))

        try:
            ct = get_objects_for_user(request.user, 'automation.change_controllertask').get(id=task)
            form = ControllerTaskForm(request.POST, instance=ct)
            if form.is_valid():
                form.save()
        except Exception:
            # new from task
            ct = ControllerTask()
            ct.controller = get_objects_for_user(request.user, 'automation.change_controller').get(id=controller)
            ct.task = get_objects_for_user(request.user, 'automation.change_task').get(id=task)
            form = ControllerTaskForm(request.POST, instance=ct)
            if form.is_valid():
                form.save()
            return render(request, 'automation/edit-controllertask.html', {'form': form, 'request_path': request.path})
    else:
        try:
            instance = get_objects_for_user(request.user, 'automation.change_controllertask').get(id=task)
            form = ControllerTaskForm(instance=instance)
        except Exception:
            ct = ControllerTask()
            ct.task = get_objects_for_user(request.user, 'automation.change_task').get(id=task)
            form = ControllerTaskForm(instance=ct)
            form.fields['task'].widget = form.fields['task'].hidden_widget()
            return render(request, 'automation/add-controllertask.html', {'form': form, 'request_path': request.path})

    return render(request, 'automation/edit-controllertask.html', {'form': form, 'request_path': request.path})


def edit_controllerdeciders(request, controller):
    if request.method == 'POST':
        provided_deciders = json.loads(request.POST.get('decider'))
        controller = get_objects_for_user(request.user, 'automation.change_controller').get(id=controller)
        for decider in controller.deciders.all():
            if decider.id not in provided_deciders:
                decider.delete()
        for decider in provided_deciders:
            cd = ControllerDecider()
            cd.decider = get_objects_for_user(request.user, 'automation.change_decider').get(id=decider)
            cd.controller = controller
            cd.save()
    return HttpResponse(json.dumps({}), content_type='application/json')


def controllers(request):
    controllers = get_objects_for_user(request.user, 'automation.change_controller').all()

    return render(request, 'automation/controllers.html', {'controllers': controllers})


def add_controller(request):
    if request.method == 'POST':
        form = ControllerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automation-controllers'))

    else:
        form = ControllerForm()
    return render(request, 'automation/add-controller.html', {'form': form})


def edit_controller(request, controller):
    controller = get_objects_for_user(request.user, 'automation.change_controller').get(id=controller)

    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            controller.delete()
            return HttpResponseRedirect(reverse('automation-controllers'))

        form = ControllerForm(request.POST, instance = controller)
        if form.is_valid():
            form.save()
    else:
        form = ControllerForm(instance = controller)

    tasks = get_objects_for_user(request.user, 'automation.change_task').all()
    deciders = get_objects_for_user(request.user, 'automation.change_decider').all()

    my_deciders = []
    for decider in controller.deciders.all():
        my_deciders.append(decider.id)

    my_tasks = ControllerTask.objects.filter(controller=controller)

    return render(request, 'automation/edit-controller.html',
                  {'form': form, 'controller': controller, 'tasks': tasks,
                   'my_tasks': my_tasks, 'deciders': deciders, 'my_deciders': my_deciders})


def deciders(request):
    deciders = get_objects_for_user(request.user, 'automation.change_decider').all()
    return render(request, 'automation/deciders.html', {'deciders': deciders})


def add_decider(request):
    if request.method == 'POST':
        form = DeciderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automation-deciders'))
    else:
        form = DeciderForm()

    return render('automation/add-decider.html', {'form': form})


def edit_decider(request, decider):
    my_decider = get_objects_for_user(request.user, 'automation.change_decider').get(id=decider)
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            my_decider.delete()
            return HttpResponseRedirect(reverse('automation-deciders'))

        form = DeciderForm(request.POST, instance=my_decider)
        if form.is_valid():
            form.save()
    else:
        form = DeciderForm(instance=my_decider)

    return render(request, 'automation/edit-decider.html', {'decider': my_decider, 'form': form})


def query_decider(request, decider):
    decider = get_objects_for_user(request.user, 'automation.change_decider').get(id=decider)
    return HttpResponse(json.dumps({"name": decider.name, "decision": decider.decide()}), content_type='application/json')


def automator_operations(request, automator):
    automator = get_objects_for_user(request.user, 'automation.change_automator').get(id=automator)

    return HttpResponse(json.dumps(automator.get_instance().get_commands()), content_type='application/json')


def edit_task(request, task):
    my_task = get_objects_for_user(request.user, 'automation.change_task').get(id=task)
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            my_task.delete()
            return HttpResponseRedirect(reverse('automation-tasks'))

        form = TaskForm(request.POST, instance=my_task)
        if form.is_valid():
            form.save()
    else:
        form = TaskForm(instance=my_task)

    return render(request, 'automation/edit-task.html', {'task': my_task, 'form': form})