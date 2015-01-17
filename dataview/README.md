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

Requests are directed to specific applications using the AppSpecificURLConfLoader middleware, located in the dataview applications middleware/router.py file. With this middleware enabled, there is no need to modify the dataview application urls.py file to include new applications.