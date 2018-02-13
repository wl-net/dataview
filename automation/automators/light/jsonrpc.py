from automation.automators import AbstractAutomator
from dataview.transports.jsonrpc import JSONRPCClient


class JSONRPCAutomator(AbstractAutomator):
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

  def turn_on(self, device, value):
    self.client.call('turn_on', arguments=[device, value])

  def turn_off(self, device):
    self.client.call('turn_off', arguments=[device])
