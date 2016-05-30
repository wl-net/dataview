
class AbstractAutomator(object):
    def __init__(self, configuration):
        self.configuration = configuration
        self.validate_configuration()

    @staticmethod
    def get_configuration_fields():
        return {}

    @classmethod
    def populate_configuration(cls, configuration={}):
        """
        Performs any automated configuration population
        :return: the current configuration
        """
        return {}

    def validate_configuration(self):
        for key in self.get_configuration_fields():
            if key not in self.configuration:
                raise ValueError("{} not provided in configuration".format(key))

    def healthcheck(self):
        pass