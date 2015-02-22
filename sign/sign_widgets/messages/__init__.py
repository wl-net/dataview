from sign.sign_widgets import AbstractWidget
import json

class MessageWidget(AbstractWidget):

    WIDGET_NAME = "Messages"

    def get_contents(self):
        return json.dumps(Message.objects.filter(user=request.user, acknowledged=False))
