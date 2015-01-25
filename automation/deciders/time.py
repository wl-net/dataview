from dataview.transports.json_rpc import JSONRPCClient
from automation.deciders import abstract
from datetime import datetime
import dateutil.parser

class TimeDecider(abstract.AbstractDecider):
    def __init__(self, conditions):
        self.conditions = conditions
        super().__init__()

    def decide(self, now=None):
        """
        determines if the current time is within the specified requirements
        """

        result = True
        if now is None:
            now = datetime.now()

        for condition in self.conditions:
            if self.__my_cmp__(now, dateutil.parser.parse(condition['time'])) not in condition['results']: 
                result = False

        return result

    def __my_cmp__(self, a, b):
        return (a > b) - (a < b)
