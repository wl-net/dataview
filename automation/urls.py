from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^automation/(?P<residence>[0-9]+)/speakers$', 'automation.views.control_speakers', name='control_speakers'),
    url(r'^automation/(?P<residence>[0-9]+)/add-speaker$', 'automation.views.add_speaker', name='add_speaker'),
    url(r'^automation/(?P<residence>[0-9]+)/edit-speaker/(?P<speaker>[0-9]+)$', 'automation.views.edit_speaker', name='edit_speaker'),
)
