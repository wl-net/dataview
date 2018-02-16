from sign.sign_updaters import AbstractSignUpdater
import requests, json


class DashingSignUpdater(AbstractSignUpdater):
    SIGN_TYPE_NAME = "Dashing"

    def update_widget(self, sign_widget):
        wi = sign_widget.widget.get_instance(sign_widget.backend_configuration)
        contents = wi.get_contents() #TODO: this must be a dict
        wconfig = json.loads(sign_widget.backend_configuration)
        if 'dashing_widget_id' not in wconfig:
            return

        self.post_to_widget(wconfig, contents)

    def post_to_widget(self, widget, payload):
        payload['auth_token'] = self.configuration['dashing_auth_token']

        r = requests.post(self.configuration['dashing_uri'] + 'widgets/' + widget['dashing_widget_id'],
                          data=json.dumps(payload))
        r.raise_for_status()

    def reload_signs(self, sign_id):
        contents = {'auth_token': self.configuration['dashing_auth_token'],
                    'event': 'reload'}

        r = requests.post(self.configuration['dashing_uri'] + 'dashboards/' + sign_id,
                          data=json.dumps(contents))
        r.raise_for_status()
