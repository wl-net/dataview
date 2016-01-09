from django.conf.urls import patterns, url

from automation.views import AutomateWizard, AutomatorForm, DeciderForm, ControllerForm
from automation.views import automators, activity, add_automator, edit_automator, run_task, index
from automation.views import controllers, add_controller, edit_controller, edit_controllertask, edit_controllerdeciders
from automation.views import deciders, add_decider, edit_decider, query_decider

urlpatterns = patterns('automation.views',
    url(r'^/?$', index, name = 'automation-index'),

    url(r'^/automate$', AutomateWizard.as_view([AutomatorForm, DeciderForm, ControllerForm], template_name='automation/automate-wizard.html')),
    url('^/run-task$', run_task, name='automation-run_task'),

    url(r'^/activity/$', activity, name='automation-activity'),

    url(r'^/automators/$', automators, name='automation-automators'),
    url('^/add-automator$', add_automator, name='automation-add_automator'),
    url('^/edit-automator/(?P<automator>[0-9a-f\-]+)$', edit_automator, name='automation-edit_automator'),

    url(r'^/controllers/$', controllers, name='automation-controllers'),
    url('^/controller$', add_controller, name='automation-add_controller'),
    url('^/controller/(?P<controller>[0-9a-f\-]+)$', edit_controller, name='automation-edit_controller'),
    url('^/controller/(?P<controller>[0-9a-f\-]+)/deciders$', edit_controllerdeciders, name='automation-edit_controllerdeciders'),

    url('^/controller/(?P<controller>[0-9a-f\-]+)/task/(?P<task>[0-9a-f\-]+)$', edit_controllertask, name='automation-edit_controllertask'),
    #url('^/controller/(?P<controller>[0-9a-f\-]+)/decider/(?P<decider>[0-9a-f\-]+)$', 'edit_controllerdecider', name='automation-edit_controllerdecider'),

    url(r'^/deciders/$', deciders, name='automation-deciders'),
    url('^/add-decider', add_decider, name='automation-add_decider'),
    url('^/edit-decider/(?P<decider>[0-9a-f\-]+)$', edit_decider, name='automation-edit_decider'),
    url('^/query-decider/(?P<decider>[0-9a-f\-]+)$', query_decider, name='automation-query_decider'),
)

