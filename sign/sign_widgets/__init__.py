
class AbstractWidget():
    """
    The AbstractWidget contains a list of methods that must be defined in widgets in order for Dataview
    to recognize the widget.
    """

    """
    The WIDGET_NAME field must be set in order for Dataview to add this widget
    """

    def __init__(self, configuration):
        self.configuration = configuration

    def get_contents(self):
        """
        get_contents should return a json object for the sign to work with
        """
        raise NotImplementedError( type(self).__name__ + " does not implement get_contents(self) " )
