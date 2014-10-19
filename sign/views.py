from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.datastructures import SortedDict
from django.http import HttpResponse, Http404

from sign.models import Sign, Widget, SignWidget

import datetime, urllib.request, json, sys
from xml.dom import minidom
from importlib import import_module

def sign(request, id=None):
    template_fields = {'widgets': []}

    try:
        sign = Sign.objects.get(id=id)
    except Sign.DoesNotExist:
        raise Http404

    for widget in sign.widgets.all():
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

    return render_to_response('sign/sign.html', RequestContext(request, template_fields))