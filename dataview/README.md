WLNet Dataview Core Application
===============================

AuthN/AuthZ
----

## Authentication requirement

Authentication is required by the use of the dataview.login_required.LoginRequiredMiddleware middlewear. Exceptions to this policy can be audited by reviewing the settings.LOGIN_EXEMPT_URLS directive.

Database Migrations
----

````
python3 manage.py makemigrations
python3 manage.py migrate
````

