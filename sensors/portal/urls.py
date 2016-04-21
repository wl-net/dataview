from django.conf.urls import patterns, url

from sensors.views import index

urlpatterns = patterns('automation.views',
    url(r'^/?$', index, name = 'sensor-index'),
)

