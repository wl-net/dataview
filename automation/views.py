from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from portal.models import Residence, Room
from automation.models import Speaker, SpeakerForm

def control_speakers(request, residence):
    speakers = Speaker.objects.filter(location = Room.objects.filter(location = Residence.objects.get(id = residence, tenants = request.user))).order_by('location')

    return render_to_response('automation/speakers.html', RequestContext(request, {'speakers': speakers}))

def add_speaker(request, residence):
    form = SpeakerForm()
    return render_to_response('automation/add-speaker.html', RequestContext(request, {'form': form}))

def edit_speaker(request, residence, speaker):
    form = SpeakerForm(instance = Speaker.objects.get(id=speaker))

    return render_to_response('automation/edit-speaker.html', RequestContext(request, {'form': form}))
