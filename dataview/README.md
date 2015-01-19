WLNet Dataview Core Application
===============================

AuthN/AuthZ
----


### Authentication requirement

Authentication is required by the use of the dataview.login_required.LoginRequiredMiddleware middlewear. Exceptions to this policy can be audited by reviewing the settings.LOGIN_EXEMPT_URLS directive.

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