from django.template import RequestContext
from django.shortcuts import render, render_to_response

# Create your views here.

def index(request):
    return render_to_response('installer/index.html', RequestContext(request, {}))


from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

class InstallWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/')