from sign.sign_widgets import AbstractWidget
from automation.models import Automator


class MediaPlayerWidget(AbstractWidget):

    WIDGET_NAME = "Media Player"

    def __init__(self, configuration):
        super().__init__(configuration)
        pass

    def get_contents(self):
        try:
            res = Automator.objects.get(id=self.configuration['automator']).get_instance().get_playback_information()
            return {'current_title': res['current']['song'], 'title': res['current']['title'],
                    'volume': res['playback_information']['volume']['numeric'],
                    'is_playing': res['playback_information']['is_playing'],
                    'position': res['playback_information']['time']['numeric'],
                    'length': res['playback_information']['length']['numeric']}
        except Exception:
            return "Unknown"

