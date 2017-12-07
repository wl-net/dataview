from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from sign.models import Sign, Widget, SignWidget

import datetime, json, sys
from importlib import import_module

from guardian.shortcuts import get_objects_for_user

def sign(request, id=None):
    template_fields = {'widgets': []}

    try:
        sign = Sign.objects.get(id=id)
    except Sign.DoesNotExist:
        raise Http404

    for signwidget in SignWidget.objects.filter(sign=sign):
        widget = signwidget.widget
        try:
            import_module("sign.widgets." + widget.internal_name)
        except Exception as e:
            print(e)
            continue
        module = sys.modules['sign.widgets.' + widget.internal_name]
        clsName = getattr(module, widget.class_name)
        cls = clsName(request)
        template_fields.update(getattr(cls, 'get_template_fields')())
        template_fields['widgets'].append({'template_path': getattr(cls, 'get_template_path')(), 'name': str(widget), 'internal_name': widget.internal_name, 'position': SignWidget.objects.get(sign=sign, widget=widget).position})

    template_fields['datetime_now'] = datetime.datetime.now()
    template_fields['x_sign_info'] = json.dumps({'signId': sign.id})

    return render_to_response('sign/sign.html', RequestContext(request, template_fields))

def sign_dashing(request, id=None):
    return render_to_response('sign/dashing-sign.html', )

def sign_config(request, id=None):
    response = {"widgets":[]}

    try:
        sign = Sign.objects.get(id=id)
    except Sign.DoesNotExist:
        raise Http404

    for signwidget in SignWidget.objects.filter(sign=sign):
        widget = signwidget.widget
        response["widgets"].append(json.loads(signwidget.frontend_configuration))

    return HttpResponse(json.dumps(response), content_type="application/json")

def sign_widget(request, id, widget_id):
    response = {}
    sw = get_objects_for_user(request.user, 'sign.change_signwidget').get(id=widget_id)
    i = sw.widget.get_instance(sw.backend_configuration)
    response['contents'] = i.get_contents()
    response['widget_name'] = i.WIDGET_NAME
    response['friendly_name'] = i.configuration['friendly_name']

    return HttpResponse(json.dumps(response), content_type="application/json")
