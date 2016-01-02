from sign.sign_widgets import AbstractWidget
from transportation.provider.opentripplanner import OpenTripPlannerProvider
import datetime

class SimpleTransportationWidget(AbstractWidget):

    WIDGET_NAME = "Departure Information"

    def __init__(self, configuration):
        super().__init__(configuration)
        self.configuration = configuration
        pass

    def get_contents(self):
        response = {}
        otpp = OpenTripPlannerProvider(self.configuration['api_target'], self.configuration['router_id'])
        plan = otpp.get_directions()
        departure_method = plan['itineraries'][0]['legs'][0]
        trip_time = round(plan['itineraries'][0]['duration']/60) 
        departure_time = plan['itineraries'][0]['legs'][0]['startTime']
        trip_efficency = SimpleTransportationWidget.get_itinerary_score(plan['itineraries'][0])
        response['trip_efficency'] = trip_efficency
        response['friendly_message'] = "{0} minutes departing at {1}".format(trip_time, datetime.datetime.fromtimestamp(int(departure_time)/1000).strftime('%H:%M'))

        return response

    def get_itinerary_score(itinerary):
        """
        this could really be anything. just factoring in the amount of spent walking, waiting and on transit.
        note that this particular implementation does not does not scale with longer trips.
        """
        return round(1/(4 / (itinerary['walkTime'] + 1)) + (2 / (itinerary['waitingTime'] + 1)) + (8 / (itinerary['transitTime'] + 1)), 2)

class TransportationWidget(AbstractWidget):

    WIDGET_NAME = "Transportation"

    def __init__(self, configuration):
        super().__init__(configuration)
        self.configuration = configuration
        pass

    def get_contents(self):
        otpp = OpenTripPlannerProvider(self.configuration['api_target'], self.configuration['router_id'])

        return otpp.get_directions()