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