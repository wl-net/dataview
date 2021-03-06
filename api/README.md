WLNet Dataview API
==================

Adding an API endpoint for a model
----

First you need to write a serializer. This should be added to serializers.py.


Example for 'User' model (included with django):

````python
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')  
````

Second, you can write a view to that determines how users will lookup the model via the API and what constraints will be enforced when filtering models. This can be added in views.py

````python
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
````

Finally, configure the URL router to allow users to reach the API at a particular location. This can be done in urls.py


````python
router.register(r'user', views.UserViewSet)
````

A list of models should now be accessible in the API. For the above example, the URL https://[DATAVIEW_HOST]/api/1/user would list all users.

Using the API
----

The API can be accessed through a web browser at /api/1. Calls to the API can be made following the pattern below:

````
curl 'http://dataview.restricted.wl-net.net:8000/api/1/<model>/' -H 'Accept: application/json'
````

Offical REST API clients are provided as part of the [dataview-rest-clients project](https://github.com/wl-net/dataview-rest-clients)