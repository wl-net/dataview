from sign.sign_widgets import AbstractWidget
from sensors.models import SensorValue

class SensorValueWidget(AbstractWidget):

    WIDGET_NAME = "Generic Sensor Value Widget"

    def get_contents(self):
        try:
            value = float(SensorValue.objects.filter(sensor=self.configuration["sensor"]).order_by('-updated')[0].value)

            if 'average' in self.configuration:
                pass

            if 'divide' in self.configuration:
                divide = self.configuration['divide']

                if 'type' in divide:
                    if 'int' == divide['type']:
                        value = int(value)

                value = value / divide['value']

            if 'round' in self.configuration:
                config = self.configuration['round']
                if 'digits' in config:
                    value = round(value, config['digits'])

            if 'minutes_to_hours' in self.configuration:
                value = int(value) / 60
                hours = int(value)
                minutes = int((value - hours) * 60)

                value = '{}:{}'.format(hours, minutes)
            return {'value': value}

        except Exception:
            return "Unknown"

      