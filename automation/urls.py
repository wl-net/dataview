from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^automation/(?P<residence>[0-9]+)/speakers$', 'automation.views.control_speakers', name='control_speakers'),
)
