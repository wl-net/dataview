WLNet Dataview Core Application
===============================

AuthN/AuthZ
----


### Authentication requirement

Authentication is required by the use of the dataview.login_required.LoginRequiredMiddleware middlewear. Exceptions to this policy can be audited by reviewing the settings.LOGIN_EXEMPT_URLS directive.

### Authorization Levels (Groups)

Several levels of access are needed:

0. Administrators
- Administrators can control all aspects of dataview. 
1. Residents
- General users are residents. They live at a primary location and interact with any number of alternate locations.
2. Service Accounts
- These act on behalf of a particular user, for example a sign needs to be able to access a user's data in order to display it.



Database Migrations
----

````
python3 manage.py makemigrations
python3 manage.py migrate
````

