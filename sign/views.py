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

    for signwidget in SignWidget.objects.filter(sign=sign).extra(order_by=['order']):
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
    return render_to_response('sign/dashing-sign.html', RequestContext(request, {}))

def sign_config(request, id=None):
  response = """/* global $, Dashboard */

    var dashboard = new Dashboard();

    dashboard.addWidget('clock_widget', 'Clock');

    dashboard.addWidget('humidity', 'Number', {
        getData: function () {
            $.extend(this.data, {
                title: 'Current Valuation',
                more_info: 'In billions',
                updated_at: 'Last updated at 14:10',
                detail: '64%',
                value: '$35'
            });
        }
    });

    dashboard.addWidget('buzzwords_widget', 'List', {
        getData: function () {
            $.extend(this.data, {
                title: 'Travel Times',
                more_info: '# of times said around the office',
                updated_at: 'Last updated at 18:58',
                data: [{label: 'Exit strategy', value: 24},
                      {label: 'Web 2.0', value: 12},
                      {label: 'Turn-key', value: 2},
                      {label: 'Enterprise', value: 12},
                      {label: 'Pivoting', value: 3},
                      {label: 'Leverage', value: 10},
                      {label: 'Streamlininess', value: 4},
                      {label: 'Paradigm shift', value: 6},
                      {label: 'Synergy', value: 7}]
            });
        }
    });

    dashboard.addWidget('convergence_widget', 'Graph', {
        getData: function () {
            $.extend(this.data, {
                title: 'Convergence',
                value: '41',
                more_info: '',
                data: [ 
                        { x: 0, y: 40 }, 
                        { x: 1, y: 49 }, 
                        { x: 2, y: 38 }, 
                        { x: 3, y: 30 }, 
                        { x: 4, y: 32 }
                    ]
                });
        }
    });""";

  return HttpResponse(response, content_type="text/javascript")
