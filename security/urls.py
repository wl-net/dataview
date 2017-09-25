from django.conf.urls import include, url

from security.views import index, safety_incidents, safety_incident_boundaries

urlpatterns = [
    url(r'^security/map$', index, name='index'),
    url(r'^security/safety-incidents$', safety_incidents),
    url(r'^security/safety-incident-boundaries$', safety_incident_boundaries),
]
