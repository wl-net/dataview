from automation.deciders import AbstractDecider
from security.models import SafetyIncident
from sensors.models import SensorValue

class SensorDecider(AbstractDecider):
    def __init__(self, conditions, configuration):
        super().__init__(conditions, configuration)

    def decide(self, now=None):
        """
        determines if the current time is within the specified requirements
        """

        result = True

        for condition in self.conditions:
            sv = SensorValue.objects.filter(sensor=self.configuration['sensor']).order_by('-updated')[0].value
            if self.__my_cmp__(float(sv), condition['value']) not in condition['results']: 
                result = False

        return result


    def __my_cmp__(self, a, b):
        return (a > b) - (a < b)
