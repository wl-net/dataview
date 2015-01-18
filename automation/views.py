from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from portal.models import Residence, Room
from automation.models import Speaker
def control_speakers(request, residence):
    speakers = Speaker.objects.filter(location = Room.objects.filter(location = Residence.objects.get(id = residence, tenants = request.user))).order_by('location')

    return render_to_response('automation/speakers.html', RequestContext(request, {'speakers': speakers}))
