from django.conf import settings
import re


class AppSpecificURLConfLoader(object):
  def __init__(self, get_response):
    self.get_response = get_response
    # One-time configuration and initialization.

  def __call__(self, request):
    """
    The goal of the application specific urlconf loader is to allow additional applications
    to be added to dataview without needing to modify the dataview application urls.py file.
    This is done by routing all requests in the form of 'https://[TARGET]/APP/some/request to
    the 'APP' application within the dataview project path.

    Only applications alphanumeric applications are supported, and they must be listed in both
    INSTALLED_APPS and DATAVIEW_APPS in order for the urlconf file to load to be overriden.
    """
    match = re.match('^/([a-zA-Z0-9]*).*', request.path)
    if match.group(1) in settings.DATAVIEW_APPS:
      request.urlconf = match.group(1) + '.urls'

    return self.get_response(request)
