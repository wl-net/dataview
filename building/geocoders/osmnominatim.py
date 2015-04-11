from building.geocoders import AbstractGeocoder
import requests

class OSMNominatim(AbstractGeocoder):
    def __init__(self):
        super().__init__()
        pass

    def geocode(self, address)
        if isinstance(address, Address):
            lookup = str(address)
        request = requests.get("https://nominatim.openstreetmap.org/search?q=%s&format=json&polygon=1&addressdetails=0" % str(address).replace(' ', '%20'))
        response = json.loads(request.content.decode('utf-8'))
        return [response[0]['lat'], response[0]['lon']]