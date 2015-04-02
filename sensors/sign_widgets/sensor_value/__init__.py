from sign.sign_widgets import AbstractWidget
from sensors.models import SensorValue

class SensorValueWidget(AbstractWidget):

    WIDGET_NAME = "Generic Sensor Value Widget"

    def __init__(self, configuration):
        super().__init__(configuration)
        pass

    def get_contents(self):
        try:
            return SensorValue.objects.filter(sensor=self.configuration["sensor"]).order_by('-updated')[0].value
        except Exception:
            return "Unknown"

      