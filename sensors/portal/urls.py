from django.conf.urls import url

from sensors.views import index, edit, observe, data

urlpatterns = [
    url(r'^/?$', index, name = 'sensor-index'),
    url(r'^/(?P<sensor>[0-9a-f\-]+)/edit$', edit, name = 'sensors-edit_sensor'),
    url(r'^/(?P<sensor>[0-9a-f\-]+)/observe$', observe, name = 'sensors-observe_sensor'),
    url(r'^/(?P<sensor>[0-9a-f\-]+)/data', data, name = 'sensors-data_sensor'),
]

