from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from portal.models import *
from security.models import Camera

# homepage
def index(request):
    return render_to_response('portal/index.html', RequestContext(request, {}))
