WLNet Dataview API
==================

Adding an API endpoint for a model
----

1. Write a serializer (serializers.py)


Example for 'User' model (included with django):

````python
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')  
````

2. Write a View (views.py)

````python
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
````

3. Configure URL router (urls.py)