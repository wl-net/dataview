from sign.sign_widgets import AbstractWidget

class TransportationWidget(AbstractWidget):

    WIDGET_NAME = "Transportation"

    def __init__(self, configuration):
        super().__init__(configuration)
        pass

    def get_contents(self):
        pass