from sign.sign_updaters import AbstractSignUpdater
from sign.models import Sign, Widget, SignWidget
import requests, json

class DashingSignUpdater(AbstractSignUpdater):
    SIGN_TYPE_NAME = "Dashing"

    def update_widget(self, sign_widget):
        wi = sign_widget.widget.get_instance(sign_widget.backend_configuration)
        contents = wi.get_contents()
        wconfig = json.loads(sign_widget.backend_configuration)
        if 'dashing_widget_id' not in wconfig:
            return
        contents['auth_token'] = self.configuration['dashing_auth_token']
        r = requests.post(self.configuration['dashing_uri'] + 'widgets/' + wconfig['dashing_widget_id'],
                          data=json.dumps(contents))
        r.raise_for_status()

    def reload_signs(self, sign_id):
        contents = {'auth_token': self.configuration['dashing_auth_token'],
                    'event': 'reload'}
        r = requests.post(self.configuration['dashing_uri'] + 'dashboards/' + sign_id,
                          data=json.dumps(contents))

        r.raise_for_status()