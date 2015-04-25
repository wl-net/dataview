from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from dataview.models import Event
from dataview.models import Account
from automation.models import Automator, Controller, Decider, AutomatorForm, ControllerForm
from automation.models import ControllerTask, ControllerTaskForm
from automation.models import ControllerDecider, DeciderForm, Task, TaskGroup

from guardian.shortcuts import get_objects_for_user

import json

def index(request):
    automators = get_objects_for_user(request.user, 'automation.change_automator')
    controllers = get_objects_for_user(request.user, 'automation.change_controller')
    deciders = get_objects_for_user(request.user, 'automation.change_decider')
    taskgroups = get_objects_for_user(request.user, 'automation.change_taskgroup')
    events = Event.objects.filter(type = 'automation.operation')[:5]
    return render_to_response('automation/index.html', RequestContext(request, {'automators': automators, 'controllers': controllers, 'deciders': deciders, 'taskgroups': taskgroups, 'events': events}))

from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

class AutomateWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/portal/automation/')

def automators(request):
    automators = get_objects_for_user(request.user, 'automation.change_automator')
    return render_to_response('automation/automators.html', RequestContext(request, {'automators': automators}))

def add_automator(request):
    if request.method == 'POST':
        form = AutomatorForm(request.POST, initial={'account': Account.objects.get(users=request.user)})
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automation-automators'))
    else:
        form = AutomatorForm(initial={'account': Account.objects.get(users=request.user)})
    return render_to_response('automation/add-automator.html', RequestContext(request, {'form': form}))

def edit_automator(request, automator):
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            get_objects_for_user(request.user, 'automation.change_automator').get(id=automator).delete()
            return HttpResponseRedirect(reverse('automation-automators'))

        form = AutomatorForm(request.POST, instance=get_objects_for_user(request.user, 'automation.change_automator').objects.get(id=automator))
        if form.is_valid():
            form.save()
    else:
        form = AutomatorForm(instance = get_objects_for_user(request.user, 'automation.change_automator').get(id=automator))
        return render_to_response('automation/add-automator.html', RequestContext(request, {'form': form}))

    return render_to_response('automation/edit-automator.html', RequestContext(request, {'form': form}))

def run_task(request):
    if request.method == 'POST':
        get_objects_for_user(request.user, 'automation.change_taskgroup').objects.get(id=request.POST.get('task')).do_operations()
    return HttpResponseRedirect(reverse('automation-index'))

def edit_controllertask(request, controller, task):
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            get_objects_for_user(request.user, 'automation.change_controllertask').get(id=task).delete()
            return HttpResponseRedirect(reverse('automation-automators'))

        try:
            ct = get_objects_for_user(request.user, 'automation.change_controllertask').objects.get(id=task)
            form = ControllerTaskForm(request.POST, instance=ct)
            if form.is_valid():
                form.save()
        except Exception:
            # new from task
            ct = ControllerTask()
            ct.controller = get_objects_for_user(request.user, 'automation.change_controller').objects.get(id=controller)
            ct.task = get_objects_for_user(request.user, 'automation.change_task').objects.get(id=task)
            form = ControllerTaskForm(request.POST, instance=ct)
            if form.is_valid():
                form.save()
            return render_to_response('automation/edit-controllertask.html', RequestContext(request, {'form': form}))

        form = ControllerTaskForm(request.POST, instance=ControllerTask.objects.get(id=task))
        if form.is_valid():
            form.save()
    else:
        try:
            instance = get_objects_for_user(request.user, 'automation.change_controllertask').objects.get(id=task)
            form = ControllerTaskForm()
        except Exception:
            ct = ControllerTask()
            ct.task = get_objects_for_user(request.user, 'automation.change_task').objects.get(id=task)
            form = ControllerTaskForm(instance=ct)
            form.fields['task'].widget = form.fields['task'].hidden_widget()
            return render_to_response('automation/add-controllertask.html', RequestContext(request, {'form': form}))

    return render_to_response('automation/edit-controllertask.html', RequestContext(request, {'form': form}))

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

    return render_to_response('automation/controllers.html', RequestContext(request, {'controllers': controllers}))

def add_controller(request):
    if request.method == 'POST':
        form = ControllerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automation-controllers'))

    else:
        form = ControllerForm()
    return render_to_response('automation/add-controller.html', RequestContext(request, {'form': form}))

def edit_controller(request, controller):
    tasks = {}
    deciders = {}
    my_tasks = {}
    my_deciders = []
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

    tasks = get_objects_for_user(request.user, 'automation.change_task').objects.all()
    deciders = get_objects_for_user(request.user, 'automation.change_decider').objects.all()

    for decider in controller.deciders.all():
        my_deciders.append(decider.id)

    my_tasks = controller.tasks.all()

    return render_to_response('automation/edit-controller.html', RequestContext(request, {'form': form, 'controller': controller, 'tasks': tasks, 'my_tasks': my_tasks, 'deciders': deciders, 'my_deciders': my_deciders}))

def deciders(request):
    deciders = get_objects_for_user(request.user, 'automation.change_decider').all()
    return render_to_response('automation/deciders.html', RequestContext(request, {'deciders': deciders}))

def add_decider(request):
    if request.method == 'POST':
        form = DeciderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automation-deciders'))
    else:
        form = DeciderForm()

    return render_to_response('automation/add-decider.html', RequestContext(request, {'form': form}))

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
        form = DeciderForm(instance = my_decider)

    return render_to_response('automation/edit-decider.html', RequestContext(request, {'decider': my_decider , 'form': form}))

def query_decider(request, decider):
      d = get_objects_for_user(request.user, 'automation.change_decider').get(id = decider)
      return HttpResponse(json.dumps({"name": d.name, "decision": d.decide()}), content_type='application/json')

