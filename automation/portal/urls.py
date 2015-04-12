from django.conf.urls import patterns, include, url

from automation.views import AutomateWizard, AutomatorForm, DeciderForm, ControllerForm

urlpatterns = patterns('automation.views',
    url(r'^/?$', 'index', name = 'automation-index'),

    url(r'^/automate$', AutomateWizard.as_view([AutomatorForm, DeciderForm, ControllerForm], template_name='automation/automate-wizard.html')),
    url('^/run-task$', 'run_task', name='automation-run_task'),

    url(r'^/automators/$', 'automators', name='automation-automators'),
    url('^/add-automator$', 'add_automator', name='automation-add_automator'),
    url('^/edit-automator/(?P<automator>[0-9a-f\-]+)$', 'edit_automator', name='automation-edit_automator'),

    url(r'^/controllers/$', 'controllers', name='automation-controllers'),
    url('^/add-controller$', 'add_controller', name='automation-add_controller'),
    url('^/edit-controller/(?P<controller>[0-9a-f\-]+)$', 'edit_controller', name='automation-edit_controller'),
    url('^/edit-controller/(?P<controller>[0-9a-f\-]+)/(?P<automator>[0-9a-f\-]+)$', 'edit_controllerautomator', name='automation-edit_controllerautomator'),

    url(r'^/deciders/$', 'deciders', name='automation-deciders'),
    url('^/add-decider', 'add_decider', name='automation-add_decider'),
    url('^/edit-decider/(?P<decider>[0-9a-f\-]+)$', 'edit_decider', name='automation-edit_decider'),
)
