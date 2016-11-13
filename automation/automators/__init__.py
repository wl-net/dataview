
class AbstractAutomator(object):
    def __init__(self, configuration):
        self.configuration = configuration
        self.validate_configuration()
        self.exposed_attributes = {}

    @staticmethod
    def get_configuration_fields():
        return {}

    def get_attributes(self):
        attributes = {}
        for attribute in self.exposed_attributes:
            attributes[attribute] = self.configuration[attribute]
        return attributes

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

    @classmethod
    def get_commands(cls):
        return {}