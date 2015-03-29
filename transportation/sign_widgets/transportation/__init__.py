from sign.sign_widgets import AbstractWidget
from transportation.provider.opentripplanner import OpenTripPlannerProvider

class TransportationWidget(AbstractWidget):

    WIDGET_NAME = "Transportation"

    def __init__(self, configuration):
        super().__init__(configuration)
        self.configuration = configuration
        pass

    def get_contents(self):
        otpp = OpenTripPlannerProvider(self.configuration['api_target'], self.configuration['router_id'])

        return ""