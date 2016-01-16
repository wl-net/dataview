from dataview.transports.json_rpc import JSONRPCClient
from automation.automators import AbstractAutomator


class RoombaRooWifiAutomator(AbstractAutomator):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])

    def clean(self):
        self.client.call('clean', [])

    def dock(self):
        self.client.call('dock', [])