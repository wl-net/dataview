import requests
import json
import time
import urllib.request as urrllib_request
import re

class GoogleMaps:
    API_ENDPOINT = "https://maps.googleapis.com/maps/api/directions/json"
    
    def directions(self, origin, destination, mode = "transit", alternatives='true', departure_time = str(int(time.time())), sensor = 'false'):
        payload = { 'origin': origin, 'destination': destination, 'mode': mode, 'alternatives': alternatives, 'departure_time': departure_time, 'sensor': sensor }
        response = requests.get(self.API_ENDPOINT, params=payload)

        if response.status_code != 200:
            response.raise_for_status()

        return json.loads(response.text)

    def test(self, origin, destination, mode = 'transit', stepNumber = 1, nested = False, alternatives = True, padding = "  "):
        response = self.directions(origin, destination, mode = mode, alternatives = alternatives)

        if (len(response) == 0):
            print("Routing failed.")
       
        routesExplored = 0
        for route in response['routes']:
            routesExplored += 1 
            for leg in route['legs']:
                if 'departure_time' in leg:
                    print("Depart at " + leg['departure_time']['text'] + " from " + leg['start_address'])
                for step in leg['steps']:
                    if step['travel_mode'] == "WALKING":
                        direction = "walk"
                        if 'html_instructions' in step:
                            direction = step['html_instructions'].replace("<b>", "").replace("</b>","").replace('<div style="font-size:0.9em">', ' (').replace('</div>', '')
                        if nested:
                            print(padding + "Substep #", end = '')
                        else:
                            print(padding + "Step #", end = '')
                        print(str(stepNumber) + ": " +direction + " ("  + step['distance']['text'] + " - " + step['duration']['text'] + ")")
                        if not nested:
                            self.test(str(step['start_location']['lat']) + ", " + str(step['start_location']['lng']), str(step['end_location']['lat']) + ", " + str(step['end_location']['lng']), mode = "walking", nested=True, alternatives=False, padding = "    ")
                    elif step['travel_mode'] == "TRANSIT":
                        oba = OneBusAway()

                        stops = oba.stops_for_location(step['start_location']['lat'], step['start_location']['lng'], radius=5)

                        if (len(stops) == 1):
                            stopId = stops[0]
                        #for agency in step['transit_details]['line']:
                        #    for 
                        direction = "Board " + step['transit_details']['line']['vehicle']['name'].lower() + " on route " + step['transit_details']['line']['short_name'] + " at stopId: " + stopId + " [" + step['transit_details']['departure_time']['text'] + "]"
                        print(padding + "Step #" + str(stepNumber) + ": " +direction + " ("  + step['distance']['text'] + " - " + step['duration']['text'] + ")")
                        stepNumber += 1
                        print(padding + "Step #" + str(stepNumber) + ": Exit bus at " + step['transit_details']['arrival_stop']['name'] + " (" + step['transit_details']['arrival_time']['text'] + ")")
                    stepNumber +=1
                if 'arrival_time' in leg:
                    print("Arrive at " + leg['end_address'] + " at " + leg['arrival_time']['text'], end="\n")
            if routesExplored != len(response['routes']):
                stepNumber = 1
                print("Alternative option #" + str(routesExplored) + ":")
        return stepNumber

class OneBusAway:
    API_ENDPOINT = "http://api.onebusaway.org/api/where/"

    def stops_for_location(self, lat, lon, radius=10):
        stops = []
        payload = { 'lat': lat, 'lon': lon, 'radius': radius, 'key': 'TEST' }
        response = requests.get(self.API_ENDPOINT + "stops-for-location.json", params=payload)

        if response.status_code != 200:
            response.raise_for_status()

        response = json.loads(response.text)
        
        for stop in response['data']['stops']:
            stops.append(stop['id'])

        return stops
            
test = GoogleMaps()
#test.test("Bellevue and Thomas Seattle 98102", "Leviathan Security Group 3220 1st ave s seattle wa")
test.test("university of washington Seattle", "Steamworks 1520 Summit Ave, Seattle, WA 98122")
