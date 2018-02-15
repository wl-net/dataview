from automation.automators import AbstractAutomator
from dataview.transports.jsonrpc import JSONRPCClient


class MusicJSONRPCAutomator(AbstractAutomator):
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

    def mute(self):
        self.client.call('mute', arguments={})

    def unmute(self):
        self.client.call('unmute', arguments={})

    def play(self, url):
        self.client.call('play', arguments = [url])
        
    def pause(self):
        self.client.call('pause', [])

    def unpause(self):
        self.client.call('unpause', [])

    def next(self):
        self.client.call('next', [])

    def previous(self):
      self.client.call('previous', [])

    def play_item(self, item):
      self.client.call('play_item', [item])

    def list(self):
      return self.client.call('list', [])

    def set_volume(self, volume):
        self.client.call('set_volume', [volume])

    def increase_volume(self, threshold=5):
        self.client.call('increase_volume', [threshold])

    def decrease_volume(self, threshold=5):
        self.client.call('decrease_volume', [threshold])

    def set_position(self, position):
        self.client.call('set_position', [position])

    def set_loop(self, status):
        self.client.call('set_loop', [status])

    def get_playback_information(self):
        return self.client.call('get_playback_information', [])

    def set_equalizer(self, band, value):
        return self.client.call('set_equalizer', [band, value])

    def set_equalizer_preamp(self, value):
        return self.client.call('set_equalizer_preamp', [value])

    def get_equalizer(self):
        return self.client.call('get_equalizer', [])