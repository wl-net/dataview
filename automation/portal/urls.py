from django.conf.urls import patterns, include, url

urlpatterns = patterns('automation.views',
    url(r'^/?$', 'index', name = 'automation-index'),
    url(r'^/(?P<residence>[0-9]+)/speakers$', 'speakers', name='automation-speakers'),
    url(r'^/(?P<residence>[0-9]+)/add-speaker$', 'add_speaker', name='add_speaker'),
    url(r'^/(?P<residence>[0-9]+)/edit-speaker/(?P<speaker>[0-9]+)$', 'edit_speaker', name='edit_speaker'),

    url(r'^/automators/$', 'automators', name='automation-automators'),
    url('^/add-automator$', 'add_automator', name='automation-add_automator'),
    url('^/edit-automator/(?P<controller>[0-9]+)$', 'edit_automator', name='automation-edit_automator'),

    url(r'^/controllers/$', 'controllers', name='automation-controllers'),
    url('^/add-controller$', 'add_controller', name='automation-add_controller'),
    url('^/edit-controller/(?P<controller>[0-9]+)$', 'edit_controller', name='automation-edit_controller'),

    url(r'^/deciders/$', 'deciders', name='automation-deciders'),
    url('^/add-decider', 'add_decider', name='automation-add_decider'),
    url('^/edit-decider/(?P<decider>[0-9]+)$', 'edit_controller', name='automation-edit_decider'),
)
