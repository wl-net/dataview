from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from dataview.models import Event
from dataview.models import Account
from automation.models import Automator, Controller, Decider, AutomatorForm, ControllerForm
from automation.models import ControllerTask, ControllerTaskForm, ControllerDecider
from automation.models import ControllerDeciderForm, DeciderForm, Task, TaskGroup

import json

def index(request):
    automators = Automator.objects.all()
    controllers = Controller.objects.all()
    deciders = Decider.objects.all()
    taskgroups = TaskGroup.objects.all()
    events = Event.objects.filter(type = 'automation.operation')[:5]
    return render_to_response('automation/index.html', RequestContext(request, {'automators': automators, 'controllers': controllers, 'deciders': deciders, 'taskgroups': taskgroups, 'events': events}))

from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

class AutomateWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/portal/automation/')

def automators(request):
    automators = Automator.objects.all()
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
            Automator.objects.get(id=automator).delete()
            return HttpResponseRedirect(reverse('automation-automators'))

        form = AutomatorForm(request.POST, instance=Automator.objects.get(id=automator))
        if form.is_valid():
            form.save()
    else:
        form = AutomatorForm(instance = Automator.objects.get(id=automator))
        return render_to_response('automation/add-automator.html', RequestContext(request, {'form': form}))

    return render_to_response('automation/edit-automator.html', RequestContext(request, {'form': form}))

def run_task(request):
    if request.method == 'POST':
        TaskGroup.objects.get(id=request.POST.get('task')).do_operations()
    return HttpResponseRedirect(reverse('automation-index'))

def edit_controllertask(request, controller, task):
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            ControllerTask.objects.get(id=task).delete()
            return HttpResponseRedirect(reverse('automation-automators'))

        try:
            ct = ControllerTask.objects.get(id=task)
            form = ControllerTaskForm(request.POST, instance=ct)
            if form.is_valid():
                form.save()
        except Exception:
            # new from task
            ct = ControllerTask()
            ct.controller = Controller.objects.get(id=controller)
            ct.task = Task.objects.get(id=task)
            form = ControllerTaskForm(request.POST, instance=ct)
            if form.is_valid():
                form.save()
            return render_to_response('automation/edit-controllertask.html', RequestContext(request, {'form': form}))

        form = ControllerTaskForm(request.POST, instance=ControllerTask.objects.get(id=task))
        if form.is_valid():
            form.save()
    else:
        try:
            instance = ControllerTask.objects.get(id=task)
            form = ControllerTaskForm()
        except Exception:
            ct = ControllerTask()
            ct.task = Task.objects.get(id=task)
            form = ControllerTaskForm(instance=ct)
            form.fields['task'].widget = form.fields['task'].hidden_widget()
            return render_to_response('automation/add-controllertask.html', RequestContext(request, {'form': form}))

    return render_to_response('automation/edit-controllertask.html', RequestContext(request, {'form': form}))


def controllers(request):
    controllers = Controller.objects.all()

    return render_to_response('automation/controllers.html', RequestContext(request, {'controllers': controllers}))

def add_controller(request):
    if request.method == 'POST':
        form = ControllerForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ControllerForm()
    return render_to_response('automation/add-controller.html', RequestContext(request, {'form': form}))

def edit_controller(request, controller):
    tasks = {}
    deciders = {}
    my_tasks ={}
    my_deciders = []
    controller = Controller.objects.get(id=controller)

    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            controller.delete()
            return HttpResponseRedirect(reverse('automation-controllers'))

        form = ControllerForm(request.POST, instance = controller)
        if form.is_valid():
            form.save()
    else:
        form = ControllerForm(instance = controller)
    tasks = Task.objects.all()
    deciders = Decider.objects.all()
    my_tasks = controller.tasks.all()
    for decider in controller.deciders.all():
        my_deciders.append(decider.id)

    return render_to_response('automation/edit-controller.html', RequestContext(request, {'form': form, 'tasks': tasks, 'my_tasks': my_tasks, 'deciders': deciders, 'my_deciders': my_deciders}))

def deciders(request):
    deciders = Decider.objects.all()
    return render_to_response('automation/deciders.html', RequestContext(request, {'deciders': deciders}))

def add_decider(request):
    if request.method == 'POST':
        form = DeciderForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DeciderForm()

    return render_to_response('automation/add-decider.html', RequestContext(request, {'form': form}))

def edit_decider(request, decider):
    if request.method == 'POST':
        if request.POST.get('delete') is not None:
            Decider.objects.get(id=decider).delete()
            return HttpResponseRedirect(reverse('automation-deciders'))

        form = DeciderForm(request.POST, instance=Decider.objects.get(id=decider))
        if form.is_valid():
            form.save()
    else:
        decider = Decider.objects.get(id=decider)
        form = DeciderForm(instance = decider)

    return render_to_response('automation/edit-decider.html', RequestContext(request, {'decider': decider, 'form': form}))

def query_decider(request, decider):
      d = Decider.objects.get(id = decider)
      return HttpResponse(json.dumps({"name": d.name, "decision": d.decide()}), content_type='application/json')

