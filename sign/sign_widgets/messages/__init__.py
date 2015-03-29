from sign.sign_widgets import AbstractWidget
from portal.models import Message
import json
from django.core import serializers

class MessageWidget(AbstractWidget):

    WIDGET_NAME = "Messages"

    def __init__(self, configuration):
        super().__init__(configuration, None)
        pass

    def get_contents(self):
        return serializers.serialize("json", Message.objects.filter(user=self.configuration["user"], acknowledged=False).all())
