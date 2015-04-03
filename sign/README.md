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

# How to get data to signs

Dataview defines two mechanisms for updating signs. First, Dataview defines the concept of a sign updater and a sign type. The sign is a required field of each sign and creates a relationship between signs and a method to update the sign. Legacy workflows may find it helpful to ask dataview for the latest information. For these cases, Dataview provides an endpoint which can be queried.

## Sign Updaters

Sign updaters are python classes that live within an application's sign_updaters folder. Each sign_updater must extend the AbstractSignUpdater class and must be linked to a sign using a sign type (see above)


## Pulling data from a widget

You can access a sign widget by requesting

/sign/*SIGN_ID*/widgets/*SIGN_WIDGET_ID*

a JSON response will be returned. As an example:

<pre>
{"friendly_name": "Directions to 3rd and Spring", "widget_name": "Departure Information", "contents": {"trip_efficency": 97.46, "friendly_message": "10 minutes departing at 13:27"}}
</pre>

the sign can poll this endpoint for data and update accordingly.

# Setting up Dashing

<pre>
$ sudo apt-get installl ruby ruby-dev bundler nodejs
$ sudo gem install dashing
$ dashing new dataview_sign
$ cd dataview_sign
$ bundle
$ dashing start
</pre>

Routing requests to /sign/id/dashing to the dashing dashboard.

<pre>
ProxyPass /sign/dataview-1 http://localhost:3030/dataview-1
ProxyPass /assets http://localhost:3030/assets
ProxyPass /views http://localhost:3030/views
ProxyPass /sign/events http://localhost:3030/events
</pre>

<pre>
RewriteEngine on
RewriteRule ^/sign/([0-9]*)/dashing$ http://localhost/sign/dataview-$1 [P]
RewriteRule ^/sign/([0-9]*)/events$ http://localhost/sign/events [P]
</pre>

# Dashing Integration

## Making changes to dashing configuration

Dataview pushes changes to the dashing dashboard erb files via a generator.

## Protecting Dashing

If dashing is run outside of Dataview, a modification to dashing will be required to ensure that dataview's authentication and authorization requirements are met. If you choose to run dashing outside of dataview, it is recommended that you use Apache and setup a ProxyPass and RewriteRule for the sign to be accessed.

### AuthN/AuthZ via Dataview

By default the dashing sign will establish a connection back to dataview with the cookies the user provided in order to determine whether or not they are authorized to view the sign.

The helper code for authorization works similar to this:

````ruby
helpers do
  def protected!
    clnt = HTTPClient.new
    clnt.cookie_manager
    if not request.cookies.has_key?('sessionid') or clnt.get('http://localhost/sign/1/dashing', nil, {'Cookie' => 'sessionid=' + request.cookies['sessionid']}).status != 200
      redirect '/account/login'
    end
    end
end
````

## Pushing updates to the sign

If dashing is used with server sent events (SSE) then dataview's `--update-sign' method must be called. This should be ran at least once a minute so that dataview can perform updates to the sign. If an application requires more frequent updates to the sign, it will push updates outside of this system.