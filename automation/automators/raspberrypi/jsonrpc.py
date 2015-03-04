from dataview.transports.json_rpc import JSONRPCClient
from automation.automators import AbstractAutomator

class RaspberryPiJSONRPCAutomator(AbstractAutomator):
    def __init__(self, configuration):
        super().__init__()
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])

    def turn_display_off(self):
        self.client.call('turn_display_off',[])
        
    def turn_display_on(self):
        self.client.call('turn_display_on',[])
