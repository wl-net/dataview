from automation.deciders import AbstractDecider
from django.core.cache import cache

from datetime import datetime
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError
import pytz
import requests
import hashlib
from icalendar import Calendar, Event
from dateutil.relativedelta import *
from dateutil.rrule import *
from dateutil.parser import *


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

    def decide(self, now=None):
        calendar = self.get_calendar()

        if 'default_reason' in self.configuration:
            self.reason = self.configuration['default_reason']

        if 'timezone' not in self.configuration:
            now = datetime.now(pytz.utc)
        else:
            try:
                now = datetime.now(timezone(self.configuration['timezone']))
                tz = timezone(self.configuration['timezone'])
            except UnknownTimeZoneError as e:
                raise AbstractDecider.ConfigurationException("pytz: Invalid timezone: " + str(e))

        for event in calendar.walk('vevent'):
            start = event.get('dtstart').dt.astimezone(timezone(self.configuration['timezone']))
            end = event.get('dtend').dt.astimezone(timezone(self.configuration['timezone']))
            time = end - start
            rule = event.get('rrule')
            if not rule:
                if now > start and now < end:
                    self.reason = str(event.get('summary'))
                    return True
                else:
                    continue

            now = now.replace(tzinfo=None)
            # exdate = event.get('EXDATE')
            # if exdate:
            #     print(str(exdate.dts))
            tz = timezone(self.configuration['timezone'])
            start= start.replace(tzinfo=None)

            rrules_start = rrulestr(rule.to_ical().decode('utf-8'), dtstart=start, ignoretz=True)

            # rrules_set = rruleset(rrules_start)
            # rrules_set.exdate(exdate)

            recurring_start = rrules_start.before(now)

            if not recurring_start:
                continue

            recurring_end = recurring_start + time

            if now > recurring_start and now < recurring_end and (recurring_end - recurring_start == time):
                self.reason = str(event.get('summary'))
                return True

        return False
