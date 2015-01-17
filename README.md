WLNet Dataview
==============

WLNet dataview provides a way to collect, interact, and view data. Dataview is being developed as a solution to home automation, though other use-cases such as office building management will not be difficult to realize.

Requirements
----

* Python 3.4+ with web hosting capabilities (mod_wsgi)
* django_rest_framework module

Installation
----

See https://github.com/wl-net/dataview/wiki/Installation

API
----

The API application provides a REST web service for interacting with dataview from third-party applications.

Automation
----

The automation application provides users with a way to automate lighting, music, and other systems in a residence.

Dataview
----

The dataview application contains shared code used by all other applications

Money
----

The money application provides basic budgeting and transactions through imported data.

Portal
----

The portal application provides users with a means to interact with the data on their laptop, smartphone, or tablet.

Security
----

The security application provides management of security cameras and records information about public safety incidents.

Sign
----

WLNet dataview provides a sign interface for dedicated systems to provide information. Sign modules should never require user interaction and should automatically update to show new information as it becomes available.

An initial version of the sign interface was built using a framework utilizing custom HTML widgets and javascript to perform client side updates. A second iteration of this sign system is under development and is based off of the "dashing" dashboard framework.

Transportation
--------------------

WLNet dataview provides a system to provide real-time information about transportation options, with an emphasis on public transportation.

Your own Application?
----

Currently if you want to deploy your own code on top of dataview you'll want to create a new django app (using python manage.py startapp within the main dataview project). To allow requests to route to your application, place your application name in DATAVIEW_APPS in settings.py. The handling of static files is currently left to the decision of the app creator.
