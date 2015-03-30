from dataview.transports.json_rpc import JSONRPCClient
from automation.automators import AbstractAutomator

class MusicJSONRPCAutomator(AbstractAutomator):
    def __init__(self, configuration):
        super().__init__()
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])

    def get_configuration_fields():
        fields = {
            'target': ['text', 'url'],
            'token': ['text', 'secret'],
            'certificate': ['text', 'pemfile'],
        }

        return fields

    def mute(self):
        self.client.call('mute',arguments={})

    def unmute(self):
        self.client.call('unmute',arguments={})

    def play(self, url):
        self.client.call('play', arguments = [url])
        
    def pause(self):
        self.client.call('pause', [])
        
    def set_volume(self, volume):
        self.client.call('set_volume', [volume])
        
    def get_playback_information(self):
        return self.client.call('get_playback_information', [])
    