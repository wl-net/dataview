from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from dataview.models import Event
from dataview.models import Account
from automation.models import Automator, Controller, Decider, AutomatorForm, ControllerForm, DeciderForm

def index(request):
    automators = Automator.objects.all()
    controllers = Controller.objects.all()
    deciders = Decider.objects.all()
    events = Event.objects.filter(type = 'automation.operation')[:5]
    return render_to_response('automation/index.html', RequestContext(request, {'automators': automators, 'controllers': controllers, 'deciders': deciders, 'events': events}))

from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

class AutomateWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/portal/automation/')

def automators(request):
    automators = Automator.objects.all()
    return render_to_response('automation/automators.html', RequestContext(request, {'form': form}))


def add_automator(request):
    if request.method == 'POST':
        form = AutomatorForm(request.POST, initial={'account': Account.objects.get(users=request.user)})
        if form.is_valid():
            form.save()
    else:
        form = AutomatorForm(initial={'account': Account.objects.get(users=request.user)})

    return render_to_response('automation/add-automator.html', RequestContext(request, {'form': form}))

def edit_automator(request, automator):
    if request.method == 'POST':
        form = AutomatorForm(request.POST, instance=Automator.objects.get(id=automator))
        if form.is_valid():
            form.save()
    else:
        form = AutomatorForm(instance = Automator.objects.get(id=automator))

    return render_to_response('automation/edit-automator.html', RequestContext(request, {'form': form}))

def controllers(request):
    controllers = Controller.objects.all()

    return render_to_response('automation/controllers.html', RequestContext(request, {'controllers': controllers}))

def add_controller(request):
    form = ControllerForm()
    return render_to_response('automation/add-controller.html', RequestContext(request, {'form': form}))

def edit_controller(request, controller):
    if request.method == 'POST':
        form = ControllerForm(request.POST, instance= Controller.objects.get(id=controller))
        if form.is_valid():
            form.save()
    else:
        form = ControllerForm(instance = Controller.objects.get(id=controller))

    return render_to_response('automation/edit-controller.html', RequestContext(request, {'form': form}))

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
        form = DeciderForm(request.POST, instance=Decider.objects.get(id=decider))
        if form.is_valid():
            form.save()
    else:
        form = DeciderForm(instance = Decider.objects.get(id=decider))

    return render_to_response('automation/edit-decider.html', RequestContext(request, {'form': form}))
