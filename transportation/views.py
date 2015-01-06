from django.shortcuts import render
from django.http import HttpResponse
import json

from portal.models import Address, DestinationGroup, Destination

def destinations(request, id=None):
    destinations = []
    for d in DestinationGroup.objects.get(pk = id).destinations.all():
        if d.is_open():
            if d.location.geo is not None:
                print(d.location.geo.coords[0])
                destinations.append([d.name, "::" + str(d.location.geo.coords[0]) + ","+ str(d.location.geo.coords[1])])

    return HttpResponse(json.dumps(destinations), content_type='application/json')
