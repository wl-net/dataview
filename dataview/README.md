WLNet Dataview Core Application
===============================

What's in Core?
----

Dataview Core contains functionality that is intended to be used in many types of deployments and is not tied to a specific service or deployment:

* Automation (Automators, Deciders, and Controllers)
* Sign
* Portal
* Sensors
* Security

Applications listed here are likely to be broken out into their own github projects and removed from the dataview project.

AuthN/AuthZ
----

### Authentication requirement

Authentication is required by the use of the dataview.login_required.LoginRequiredMiddleware middleware. Exceptions to this policy can be audited by reviewing the settings.LOGIN_EXEMPT_URLS directive.

### Authorization Levels (Groups)

Several levels of access are needed:

* Administrators

Administrators can control all aspects of dataview. 

* Residents

General users are residents. They live at a primary location and interact with any number of alternate locations.

* Service Accounts

These act on behalf of a particular user, for example a sign needs to be able to access a user's data in order to display it.



Database Migrations
----

````
python3 manage.py makemigrations
python3 manage.py migrate
````

Runing Tests
----
````
python3 manage.py test
````

UUID Backed Models
----

To help prevent enumeration, uuid based models are encouraged. Please extend new models off of dataivew.common.models.UUIDModel instead of the standard django.db.models.Model. If you need you add a uuid pk to a model based on some other class, please review the dataview.common.models package first.

Request Routing
----

Requests are directed to specific applications using the AppSpecificURLConfLoader middleware, located in the dataview applications middleware/router.py file. With this middleware enabled, there is no need to modify the dataview application urls.py file to include new applications. Applications that rely on [application]/urls.py can will only be routed to when request of is of the form 'GET /application'. In order to route requests that do not meet this requirement, the application must be listed in the GLOBAL_URLCONF settings.py directive. For applications that only need to exist within the portal, the DATAVIEW_APPS directive will suffice - however a valid urlconf file must be present in application/portal/urls.py

An example portal/urls.py:

````python
from django.conf.urls import patterns, url

urlpatterns = patterns('automation.views',
    url(r'^/?$', 'index', name = 'automation-index'), # this matches portal/automation and portal/automation/
    url(r'^/(?P<residence>[0-9]+)/speakers$', 'speakers', name='automation-speakers'),
    url(r'^/(?P<residence>[0-9]+)/add-speaker$', 'add_speaker', name='add_speaker'),
    url(r'^/(?P<residence>[0-9]+)/edit-speaker/(?P<speaker>[0-9]+)$', 'edit_speaker', name='edit_speaker'),
)
````

**Note:** The portal application processes only portal/application, so your requests should expect (and require) a '/'.

Static Files
----

Create a "static" folder under your application (for example, sign/static). Place any files your application needs within another folder with the same name as your application:

<pre>
$ ls sign/static/sign/ -R
sign/static/sign/:
js

sign/static/sign/js:
dashing.js
</pre>

The **collectstatic** command can be used to make the static files accessible:

<pre>
python3 manage.py collectstatic
</pre>

Core Transports
----

Dataview will support several transports to communicate with external systems (such as automation devices, used in the automation application). The initial release will only support JSON-RPC (2.0).