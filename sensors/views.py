from django.template import RequestContext
from django.shortcuts import render, render_to_response

from guardian.shortcuts import get_objects_for_user


def index(request):
    sensors = get_objects_for_user(request.user, 'sensors.change_sensor')

    return render_to_response('sensors/index.html',
                              RequestContext(request, {'sensors': sensors}))
