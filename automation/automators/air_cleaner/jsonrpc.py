from automation.automators import AbstractAutomator
from dataview.transports.json_rpc import JSONRPCClient


class AirCleanerJSONRPCAutomator(AbstractAutomator):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])

    def set_fan_speed(self, fan_speed):
        self.client.call('call_function', ['acfanspeed', [fan_speed.upper()]])

    def get_commands(self):
        return {"set_fan_speed":{"args":[["off", "low", "medium", "high"]]}}
