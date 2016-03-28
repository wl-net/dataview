class AbstractDecider(object):
    class CommunicationException(Exception):
        pass

    class ConfigurationException(Exception):
        pass

    def __init__(self, conditions, configuration={}):
        self.conditions = conditions
        self.configuration = configuration
        self.validate_configuration()

    @staticmethod
    def get_configuration_fields():
        return {}

    def validate_configuration(self):
        for key in self.get_configuration_fields():
            if key not in self.configuration:
                raise ValueError("{} not provided in configuration".format(key))


    def decide(self):
        """
        Determines the outcome of the decider.
        """
        return False

    def fuzzy_decide(self):
        """
        Returns a numeric value representing the outcome of the decider (integers between 0-1)
        """
        return int(self.decide())

    def get_decision_reason(self):
        """
        Returns a list of decisions and their results.
        """
