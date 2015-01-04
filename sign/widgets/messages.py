from sign.widgets.abstractwidget import AbstractWidget
from portal.models import Message

class Messages(AbstractWidget):

    def get_template_fields(self):
        if self.request.user.is_authenticated():
            return {'message_messages': Message.objects.filter(user=self.request.user, acknowledged=False)}
        return {}
    
    def get_template_path(self):
        return "sign/widgets/messages.html"
