from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from portal.models import Residence, Room, Event
from automation.models import Automator, Controller, Decider, AutomatorForm, ControllerForm, DeciderForm, Speaker, SpeakerForm

def index(request):
    automators = Automator.objects.all()
    controllers = Controller.objects.all()
    deciders = Decider.objects.all()
    events = Event.objects.filter(type = 'automation.operation')[:5]
    return render_to_response('automation/index.html', RequestContext(request, {'automators': automators, 'controllers': controllers, 'deciders': deciders, 'events': events}))

def speakers(request, residence):
    speakers = Speaker.objects.filter(location = Room.objects.filter(location = Residence.objects.get(id = residence, tenants = request.user))).order_by('location')

    return render_to_response('automation/speakers.html', RequestContext(request, {'speakers': speakers}))

def add_speaker(request, residence):
    form = SpeakerForm()
    return render_to_response('automation/add-speaker.html', RequestContext(request, {'form': form}))

def edit_speaker(request, residence, speaker):
    form = SpeakerForm(instance = Speaker.objects.get(id=speaker))

    return render_to_response('automation/edit-speaker.html', RequestContext(request, {'form': form}))

def automators(request):
    automators = Automator.objects.all()
    return render_to_response('automation/automators.html', RequestContext(request, {'form': form}))


def add_automator(request):
    if request.method == 'POST':
        form = AutomatorForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AutomatorForm()

    return render_to_response('automation/add-automator.html', RequestContext(request, {'form': form}))

def edit_automator(request, automator):
    if request.method == 'POST':
        form = AutomatorForm(request.POST, instance= Atuomator.objects.get(id=automator))
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
    return render_to_response('automation/deciders.html', RequestContext(request, {'form': form}))

def add_decider(request):
    return render_to_response('automation/add-decider.html', RequestContext(request, {'form': form}))

def edit_decider(request, decider):
    return render_to_response('automation/edit-decider.html', RequestContext(request, {'form': form}))
