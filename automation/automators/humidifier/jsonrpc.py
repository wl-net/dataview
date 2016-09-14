from dataview.transports.jsonrpc import JSONRPCClient
from automation.automators import AbstractAutomator


class HumidiferJSONRPCAutomator(AbstractAutomator):

    def __init__(self, configuration):
        super().__init__(configuration)
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])

    @staticmethod
    def get_configuration_fields():
        fields = {
            'target': ['text', 'url'],
            'token': ['text', 'secret'],
            'certificate': ['text', 'pemfile'],
        }

        return fields

    def set_fan_speed(self, fan_speed):
        self.client.call('call_function', ['humfanspeed', [fan_speed.upper()]])

    def set_output_rate(self, output_rate):
        self.client.call('call_function', ['humoutrate', [output_rate.upper()]])

    def get_commands(self):
        return {"set_fan_speed":{"args":[["off", "high", "low"]]}, "set_output_rate":{"args":[["off", "high", "low"]]}}

    def healthcheck(self):
        self.client.call({'healthcheck', []})