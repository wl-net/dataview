from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from security.models import SafetyIncidentAlert, SafetyIncidentAlertBoundary
import datetime, json


def index(request):
    return render_to_response('security/map.html', RequestContext(request, {}))


def safety_incidents(request):
    incidents = []
    sabs = SafetyIncidentAlertBoundary.objects.all()

    for sab in sabs:
        for sia in SafetyIncidentAlert.objects.filter(boundary=sab, incident__time__gte= datetime.datetime.now() - datetime.timedelta(hours=6)):
            incident = sia.incident
            incidents.append({'location': incident.location,
                              'geolocation': [incident.geo.y, incident.geo.x],
                              'units': incident.units, 'type': incident.type})
    return HttpResponse(json.dumps(incidents), content_type='application/json')


def safety_incident_boundaries(request):
    boundaries = []

    for sab in SafetyIncidentAlertBoundary.objects.filter(enabled=True):
        boundaries.append({'name': sab.name, 'coordinates': sab.geobox.tuple})

    return HttpResponse(json.dumps(boundaries), content_type='application/json')
