from automation.deciders import AbstractDecider
from django.core.cache import cache

from datetime import datetime, timezone
import requests
import hashlib
from icalendar import Calendar, Event
from dateutil.relativedelta import *
from dateutil.rrule import *


class CalendarDecider(AbstractDecider):
    CACHE_TIME = 5 * 60

    def __init__(self, conditions, configuration):
        self.reason = ""
        super().__init__(conditions, configuration)

    @staticmethod
    def get_configuration_fields():
        fields = {
            'ical_url': ['text', 'url'],
        }

        return fields

    def get_calendar(self):
        index = 'ical_' + hashlib.sha256(self.configuration['ical_url'].encode('utf-8')).hexdigest()
        response = cache.get(index)

        if not response:
            request = requests.get(self.configuration['ical_url'])
            request.raise_for_status()

            response = request.text
            cache.set(index, response, self.CACHE_TIME)

        return Calendar.from_ical(response)

    def get_decision_reason(self):
        return self.reason

    def decide(self, now=datetime.now(timezone.utc)):
        calendar = self.get_calendar()

        for event in calendar.walk('vevent'):
            start = event.get('dtstart').dt
            end = event.get('dtend').dt
            time = end - start
            rrule = event.get('rrule')

            #exdate = event.get( 'EXDATE' ) # TODO
            rrules_start = rrulestr(rrule.to_ical().decode("utf-8"), dtstart=start)
            reccuring_start = rrules_start.before(now)

            reccuring_end = reccuring_start + time

            if now > reccuring_start and now < reccuring_end and (reccuring_end - reccuring_start == time):
                self.reason = str(event.get('summary'))
                return True

        return False

