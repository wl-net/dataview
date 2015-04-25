from automation.deciders import AbstractDecider
from security.models import SafetyIncident
from sensors.models import SensorValue

class SensorDecider(AbstractDecider):
    def __init__(self, conditions, configuration):
        super().__init__(conditions, configuration)

    def decide(self, now=None):
        """
        determines if the current sensor value is within the specified requirements
        """

        result = True
        self.reason = []

        for condition in self.conditions:
            sv = SensorValue.objects.filter(sensor=self.configuration['sensor']).order_by('-updated')[0].value
            if self.__my_cmp__(float(sv), condition['value']) not in condition['results']: 
                self.reason.append({'message': 'comparison of {0} was {2} {1}'.format(float(sv), condition['value'], self.__get_cmp_str__(self.__my_cmp__(float(sv), condition['value']))) })
                result = False
            else:
                self.reason.append({'message': 'comparison of {0} was {2} {1}'.format(float(sv), condition['value'], self.__get_cmp_str__(self.__my_cmp__(float(sv), condition['value']))) })


        return result

    def get_decision_reason(self):
        return self.reason

    def __my_cmp__(self, a, b):
        return (a > b) - (a < b)

    def __get_cmp_str__(self, res):
        strs = {-1: "less than", 0: "equal", 1: "greater than"}
        return strs[res]