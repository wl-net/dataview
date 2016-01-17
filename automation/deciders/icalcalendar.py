from automation.deciders import AbstractDecider
from datetime import datetime, timezone

import requests
from icalendar import Calendar, Event
from dateutil.relativedelta import *
from dateutil.rrule import *


class CalendarDecider(AbstractDecider):
    def __init__(self, conditions, configuration):
        self.conditions = conditions
        self.reason = ""
        super().__init__(conditions, configuration)

    def get_calendar(self):
        request = requests.get(self.configuration['ical_url'])
        request.raise_for_status()

        return Calendar.from_ical(request.text)

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

            rrules_end = rrulestr(rrule.to_ical().decode("utf-8"), dtstart=end)
            reccuring_end = rrules_end.after(now)

            if now > reccuring_start and now < reccuring_end and (reccuring_end - reccuring_start == time):
                self.reason = str(event.get('summary'))
                return True

        return False

