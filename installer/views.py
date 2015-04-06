from django.shortcuts import render

# Create your views here.

def index(request):
    pass

from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

class InstallWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/')