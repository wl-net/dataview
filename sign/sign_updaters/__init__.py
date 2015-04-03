from sign.models import SignWidget

class AbstractSignUpdater:
    def __init__(self, configuration):
        self.configuration = configuration
        pass

    def update_widget(self, sign_widget):
        pass