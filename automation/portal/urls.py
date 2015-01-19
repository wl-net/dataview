from django.conf.urls import patterns, include, url

urlpatterns = patterns('automation.views',
    url(r'(?P<residence>[0-9]+)/speakers$', 'control_speakers', name='control_speakers'),
    url(r'(?P<residence>[0-9]+)/add-speaker$', 'add_speaker', name='add_speaker'),
    url(r'(?P<residence>[0-9]+)/edit-speaker/(?P<speaker>[0-9]+)$', 'edit_speaker', name='edit_speaker'),
    
    url(r'^automation/(?P<residence>[0-9]+)/speakers$', 'control_speakers', name='control_speakers'),
)
