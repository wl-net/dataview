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