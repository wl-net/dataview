from sign.sign_widgets import AbstractWidget

class SensorValueWidget(AbstractWidget):

    WIDGET_NAME = "Generic Sensor Value Widget"

    def get_contents(self):
        return ""