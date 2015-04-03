from sign.sign_updaters import AbstractSignUpdater
from sign.models import Sign, Widget, SignWidget
import requests, json

class DashingSignUpdater(AbstractSignUpdater):
    SIGN_TYPE_NAME = "Dashing"

    def update_widget(self, sign_widget):
        wi = sign_widget.widget.get_instance(sign_widget.backend_configuration)
        contents = wi.get_contents()
        wconfig = json.loads(sign_widget.backend_configuration)
        if 'dashing_view_type_identifier' not in wconfig:
            return      
        r = requests.post(self.configuration['dashing_uri'] + 'widgets/' + sign_widget.widget.external_id,
                          data=json.dumps({'auth_token': self.configuration['dashing_auth_token'], json.loads(sign_widget.backend_configuration)['dashing_view_type_identifier']: contents}))
        r.raise_for_status()