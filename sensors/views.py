from django.http import HttpResponse
from django.shortcuts import render

from guardian.shortcuts import get_objects_for_user

import json


def index(request):
    sensors = get_objects_for_user(request.user, 'sensors.change_sensor')

    return render(request, 'sensors/index.html', {'sensors': sensors})


def edit(request, sensor):
    sensor = get_objects_for_user(request.user, 'sensors.change_sensor').get(id=sensor)
    return render(request, 'sensors/edit.html', {'sensor': sensor})


def observe(request, sensor):
    sensor = get_objects_for_user(request.user, 'sensors.change_sensor').get(id=sensor)
    values = sensor.get_values()
    return render(request, 'sensors/observe.html', {'sensor': sensor, 'values': values})


def data(request, sensor):
    sensor = get_objects_for_user(request.user, 'sensors.change_sensor').get(id=sensor)
    values = sensor.get_values(200)

    x = []
    y = []
    for value in values:
        x.append(str(value.updated))
        y.append(value.value)

    return HttpResponse(json.dumps({'data':{'x': x, 'y': y}}), content_type='application/json')
