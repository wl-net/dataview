WLNet Dataview Sign Application
===============================

# Creating Custom widgets

Create a sign_widgets folder under your application and place the following code under 'your_application/sign_widgets/your_widget/\__init\__.py':

<pre>
from sign.sign_widgets import AbstractWidget

class YourWidget(AbstractWidget):

    WIDGET_NAME = "Your Widget"

    def __init__(self, configuration):
        super().__init__(configuration)
        pass

    def get_contents(self):
        return {} # An object that the widget will consume (this will be encoded as json before sending)
</pre>

# Pulling data from a widget

You can access a sign widget by requesting

/sign/*SIGN_ID*/widgets/*SIGN_WIDGET_ID*

a JSON response will be returned. As an example:

<pre>
{"friendly_name": "Directions to 3rd and Spring", "widget_name": "Departure Information", "contents": {"trip_efficency": 97.46, "friendly_message": "10 minutes departing at 13:27"}}
</pre>

the sign can poll this endpoint for data and update accordingly.