class AbstractSignUpdater(object):
    def __init__(self, configuration):
        self.configuration = configuration
        pass

    def update_widget(self, sign_widget):
        pass

    def reload_signs(self, sign_id):
        pass