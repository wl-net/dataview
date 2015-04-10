from django.conf.urls import patterns, include, url
from dataview.models import AccountForm
from installer.views import InstallWizard

urlpatterns = patterns('',
    url(r'/welcome', 'installer.views.index', name='index'),       
    url(r'/install', InstallWizard.as_view([AccountForm], template_name='installer/install-wizard.html')),
)
