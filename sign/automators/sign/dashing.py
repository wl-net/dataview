from automation.automators import AbstractAutomator

from sign.sign_updaters.dashing import DashingSignUpdater
from sign.models import Sign


class DashingSignAutomator(AbstractAutomator):
  def __init__(self, configuration):
    super().__init__(configuration)

  @staticmethod
  def get_configuration_fields():
    fields = {
      'dashing_widget_id': ['text'],
    }

    return fields

  def set_fade(self, value):
      sign = Sign.objects.get(id=self.configuration['sign_id'])

      sign.get_sign_updater().post_to_widget({'dashing_widget_id': 'dataview-core'}, {'fade_value': value})
