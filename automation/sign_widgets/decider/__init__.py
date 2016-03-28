from sign.sign_widgets import AbstractWidget
from automation.models import Decider


class DeciderWidget(AbstractWidget):
    WIDGET_NAME = "Decider"

    def get_contents(self):
        try:
            instance = Decider.objects.get(id=self.configuration["decider"]).get_instance()
            instance.decide()
            return {'text': instance.get_decision_reason()}
        except Exception as e:
            return {"text": None, "error":  str(e)}
