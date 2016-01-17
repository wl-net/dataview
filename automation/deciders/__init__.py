class AbstractDecider:
    def __init__(self, conditions, configuration={}):
        self.conditions = conditions
        self.configuration = configuration

    def decide(self):
        """
        Determines the outcome of the decider.
        """
        return False

    def fuzzy_decide(self):
        """
        Returns a numeric value representing the outcome of the decider (integers between 0-1)
        """
        return int(self.decide())

    def get_decision_reason(self):
        """
        Returns a list of decisions and their results.
        """
