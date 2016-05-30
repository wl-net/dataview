from dataview.transports.jsonrpc import JSONRPCClient
from automation.automators import AbstractAutomator


class RaspberryPiJSONRPCAutomator(AbstractAutomator):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])

    @classmethod
    def populate_configuration(cls, configuration={}):
        if 'token' not in configuration:
            configuration['token'] = JSONRPCClient.generate_random_token()

        return configuration

    def turn_display_off(self):
        self.client.call('turn_display_off',[])
        
    def turn_display_on(self):
        self.client.call('turn_display_on',[])
