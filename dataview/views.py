from django.shortcuts import render
from django.http import HttpResponse
import json

def v1_config(request):
    config = {
        'dataview': {
            'username': request.user.username,
            'my_location': '',
            'my_location_latlng': []
        },
    }

    return HttpResponse(json.dumps(config), content_type='application/json')
