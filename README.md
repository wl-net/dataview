WLNet Dataview [![Build Status](https://travis-ci.org/wl-net/dataview.svg?branch=master)](https://travis-ci.org/wl-net/dataview)
==============

# Warning: This project is being phased out in favor of Arcus (wl-net/arcusplatform)

WLNet dataview provides a way to collect, interact, and view data. Dataview is being developed as a solution to home automation, though other use-cases such as office building management will not be difficult to realize. The official website for dataview is located at http://opensource.wl-net.net/projects/dataview

Is Dataview for You?
---

Dataview is currently under development and doens't offer a lot of functionality to users who are not interested in developing on top of it. If you are interested in automation, this might be a good platform to build off of.

Project Status
----

WLNet Dataview is being developed under WLNet's Open Source program and is still nearing a stable release. Upgrading from public revisions of dataview is not supported, but will work in most cases as long as database migrations are made and performed.

Requirements
----

* Python 3.4+ with web hosting capabilities (mod_wsgi)
* django 1.8
* Postgres database with PostGIS support

For a list of required third-party libraries, please refer to the Installation page.

Installation
----

See https://github.com/wl-net/dataview/wiki/Installation

TLDR:

<pre>
pip -r requirements.txt
cp dataview/settings.dist.py dataview/settings.py
python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
</pre>

Contributing
----

TODO

Support
----

Open a issue on GitHub or send an email to andrew@andrewsorensen.net

API
----

The API application provides a REST web service for interacting with dataview from third-party applications. The REST framework is implemented using Django REST Framework and utilizes token based authentication for ease of use in external applications.

Automation
----

The automation application provides users with a way to automate lighting, music, and other systems in a residence. This application is supplemented by the sensors application, which can provide additional information to act upon when performing automation tasks. Dataview does not support any standard automation protcols out of the box, but rather relies on Automators to translate dataview actions into native commands through a JSON-RPC interface. [Automation Documentation](https://github.com/wl-net/dataview/blob/master/automation/README.md) 

Dataview
----

The dataview application contains shared code used by all other applications.

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
--------------

WLNet dataview provides a system to provide real-time information about transportation options, with an emphasis on public transportation.


Your own Application?
----

Currently if you want to deploy your own code on top of dataview you'll want to create a new django app (using python manage.py startapp within the main dataview project). To allow requests to route to your application, place your application name in DATAVIEW_APPS in settings.py. The handling of static files is currently left to the decision of the app creator.
