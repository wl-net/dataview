from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from portal.models import *


def index(request):
    return render_to_response('portal/index.html', RequestContext(request, {}))

def dismiss_message(request):
    m = Message.objects.get(id=int(request.POST['messageid']))
    m.acknowledge()
    m.save()
    
    return HttpResponse(json.dumps({}), content_type='application/json')
