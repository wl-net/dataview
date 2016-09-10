from django.shortcuts import render
from django.http import HttpResponse
from portal.models import Message


def index(request):
    return render(request, 'portal/index.html', {})


def dismiss_message(request):
    m = Message.objects.get(id=int(request.POST['messageid']))
    m.acknowledge()
    m.save()
    
    return HttpResponse(json.dumps({}), content_type='application/json')
