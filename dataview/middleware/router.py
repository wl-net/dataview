
class AppSpecificURLConfLoader():

  def process_request(self, request):
    request.urlconf = ''
    return None
