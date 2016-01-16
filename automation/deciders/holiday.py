from automation.deciders import AbstractDecider
from datetime import datetime
import holidays


class HolidayDecider(AbstractDecider):
    def __init__(self, conditions, configuration):
        self.conditions = conditions
        super().__init__(conditions, configuration)

    def decide(self, now=None):
        """
        determines if the current date is a holiday
        """

        result = False
        if now is None:
            now = datetime.now()
        
        cur_holidays = holidays.US()
        if now in cur_holidays and cur_holidays[now] in self.conditions:
            result = True

        return result