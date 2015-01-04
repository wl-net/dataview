class AbstractWidget():
    def __init__(self, request):
        self.request = request
        pass
        self.request = request
    def get_template_fields(self):
        raise NotImplementedError( type(self).__name__ + " does not implement get_template_fields(self) " )
    def get_template_path(self):
        raise NotImplementedError( type(self).__name__ + " does not implement get_template_path(self) " )
