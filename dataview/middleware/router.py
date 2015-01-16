from django.conf import settings
import re

class AppSpecificURLConfLoader():

  def process_request(self, request):
    match = re.match('^/([a-zA-Z0-9]*).*', request.path)
    if match.group(1) in settings.INSTALLED_APPS:
      request.urlconf = match.group(1) + '.urls'
    return None
