WLNet Dataview Sign Application
===============================

# Using a sign

A general purpose computer can display the sign. WLNet has performed testing on Raspberry Pis (version 2), though other devices should be able to perform the task if they have sufficent computation power.

Simply navigate to https://YOUR_DATAVIEW_ENDPOINT/sign/SIGN_ID and the sign will be displayed. It is recommended that you enable the kiosk mode in your browser to maximize the amount of space available for sign widgets.

# Installing Widgets

When installing a widget (regardless of who created it), you will need to inform dataview that you have installed a new widget:

<pre>
wlnet@wlnet-dataview:~/dataview$ python3 manage.py signcontrol --update-widgets
</pre>

You should now see your widget in the list of available widgets.

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