from dataview.transports.json_rpc import JSONRPCClient
from automation.deciders import AbstractDecider
from datetime import datetime
import dateutil.parser

class TimeDecider(AbstractDecider):
    def __init__(self, conditions, configuration):
        self.conditions = conditions
        self.configuration = configuration
        super().__init__(conditions)

    def decide(self, now=None):
        """
        determines if the current time is within the specified requirements
        """

        result = True
        if now is None:
            now = datetime.now().time()

        for condition in self.conditions:
            if self.__my_cmp__(now, dateutil.parser.parse(condition['time']).time()) not in condition['results']: 
                result = False

        return result

    def __my_cmp__(self, a, b):
        return (a > b) - (a < b)
