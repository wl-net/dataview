class AbstractDecider:
    def __init__(self):
        pass

    def decide(self):
        """
        Determines the outcome of the decider.
        """
        return False

    def fuzzy_decide():
        """
        Returns a numeric value representing the outcome of the decider (integers between 0-1)
        """
        return int(self.decide())

    def get_decision_reason(self):
        """
        Returns a OrderedDict of decisions and their results.
        """
