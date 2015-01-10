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

Transportation
--------------------

WLNet dataview provides a system to provide real-time information about transportation options, with an emphasis on public transportation.
