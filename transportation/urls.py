from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^transportation/destinations/(?P<id>[0-9]+)$', 'transportation.views.destinations', name='destinations'),
    url(r'transportation/add-destination$', 'transportation.views.add_destination', name='add_destination'),
)
