from dataview.transports.json_rpc import JSONRPCClient
from automation.automators import AbstractAutomator

class MusicJSONRPCAutomator(AbstractAutomator):
    def __init__(self, configuration):
        super().__init__()
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])

    def mute(self):
        self.client.call('mute',arguments={})
        
    def play(self, url):
        self.client.call('play', arguments = [url])
        
    def pause(self):
        self.client.call('pause', [])
        
    def set_volume(self, volume):
        self.client.call('set_volume', [volume])
        
    def get_playback_information(self):
        self.client.call('get_playback_information', [])
    