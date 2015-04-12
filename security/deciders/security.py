from automation.deciders import AbstractDecider
from security.models import SafetyIncident

class PublicSafetyIncidentDecider(AbstractDecider):
    def __init__(self, conditions, configuration={}):
        self.conditions = conditions
        self.configuration = configuration
        super().__init__()

    def decide(self):
        """
        determines if a public safety event has occured within the given period of time
        """
        now = datetime.now()
        result = False

        for condition in self.conditions:
            then = now - datetime.timedelta(days=int(condition.minutes_back))

            if SafetyIncident.objects.filter(location=condition.location, time__lte=then).count() > 0:
                result = True

        return result
