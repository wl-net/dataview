from dataview.transports.jsonrpc import JSONRPCClient
from automation.automators import AbstractAutomator


class RaspberryPiJSONRPCAutomator(AbstractAutomator):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])
        self.exposed_attributes = {'token', 'target'}

    @classmethod
    def populate_configuration(cls, configuration={}):
        if 'token' not in configuration:
            configuration['token'] = JSONRPCClient.generate_random_token()

        return configuration

    @staticmethod
    def get_configuration_fields():
        fields = {
            'target': ['text', 'url'],
            'token': ['text', 'secret'],
            'certificate': ['text', 'pemfile'],
        }

        return fields

    @classmethod
    def get_commands(cls):
        return {'turn_display_off': {'args': []}, 'turn_display_on': {'args': []}, }

    def turn_display_off(self):
        self.client.call('turn_display_off', [])
        
    def turn_display_on(self):
        self.client.call('turn_display_on', [])

    def start_kodi(self):
        self.client.call('start_kodi', [])

    def stop_kodi(self):
        self.client.call('stop_kodi', [])