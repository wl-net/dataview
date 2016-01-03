import requests, datetime

class OpenTripPlannerProvider():
  
    def __init__(self, api_target, router_id):
        self.api_target = api_target
        self.router_id = router_id

    def get_directions(self, fromPlace, toPlace, time='', date=datetime.date.today().strftime('%m-%d-%Y'), mode='WALK,TRANSIT', maxWalkDistance = 1000, arriveBy=False, wheelchair=False, showIntermediateStops=False):
        r = requests.get(self.api_target + 'otp/routers/' + self.router_id + '/plan', params =
                     {'fromPlace': fromPlace, 'toPlace': toPlace, 'time': time, 'date': date, 'mode': mode, 'maxWalkDistance': maxWalkDistance,
                      'arriveBy': arriveBy, 'wheelchair': wheelchair, 'showIntermediateStops': showIntermediateStops}
                     , headers = {'Accept': 'application/json'})
        if r.status_code != 200:
            pass
        return r.json()['plan']