from django.conf.urls import patterns, include, url
from dataview.models import AccountForm
from installer.views import InstallWizard

urlpatterns = patterns('',
    url(r'/install', InstallWizard.as_view([AccountForm], template_name='installer/install-wizard.html')),
)
