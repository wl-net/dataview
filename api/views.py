from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import django_filters

from rest_framework import viewsets, filters
from rest_framework.response import Response

from api.serializers import UserSerializer, AddressSerializer, DestinationSerializer, GuestSerializer, MessageSerializer, OpenHourSerializer

from portal.models import Guest, Message
from building.models import Address

from transportation.models import Destination, OpenHour


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    serializer_class = UserSerializer
    queryset = User.objects.none() # critical

    def list(self, request):
        queryset = User.objects.filter(username = request.user.username) # critical
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        queryset = User.objects.filter(username = request.user.username) # critical
        guest = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(guest, context={'request': request})
        return Response(serializer.data)

# portal models



class AddressFilter(django_filters.FilterSet):
    street = django_filters.CharFilter(name="street",lookup_type="icontains")
    city = django_filters.CharFilter(name="city",lookup_type="icontains")

    class Meta:
        model = Address
        fields = ('street', 'city')


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_class = AddressFilter
    filter_backends = (filters.DjangoFilterBackend,)
    search_fields = ('street', 'city')


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    
class GuestViewSet(viewsets.GenericViewSet):
    queryset = Guest.objects.none() # critical

    def list(self, request):
        queryset = Guest.objects.filter(user = request.user) # critical
        serializer = GuestSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Guest.objects.filter(user = request.user) # critical
        guest = get_object_or_404(queryset, pk=pk)
        serializer = GuestSerializer(guest, context={'request': request})
        return Response(serializer.data)

class MessageViewSet(viewsets.GenericViewSet):
    queryset = Message.objects.none() # critical

    def list(self, request):
        queryset = Message.objects.filter(user = request.user) # critical
        serializer = MessageSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Message.objects.filter(user = request.user) # critical
        message = get_object_or_404(queryset, pk=pk)
        serializer = MessageSerializer(message, context={'request': request})
        return Response(serializer.data)

class OpenHourViewSet(viewsets.ModelViewSet):
    queryset = OpenHour.objects.all()
    serializer_class = OpenHourSerializer
    
# other applications

from sensors.models import Sensor, SensorValue
from api.serializers import SensorSerializer, SensorValueSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorValueViewSet(viewsets.ModelViewSet):
    queryset = SensorValue.objects.all()
    serializer_class = SensorValueSerializer
# security application

from security.models import Camera, SafetyIncidentSource, SafetyIncident, SafetyIncidentAlert, SafetyIncidentAlertBoundary
from api.serializers import CameraSerializer, SafetyIncidentSourceSerializer, SafetyIncidentSerializer, SafetyIncidentAlertSerializer, SafetyIncidentAlertBoundarySerializer

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class SafetyIncidentSourceViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    queryset = SafetyIncidentSource.objects.all()
    serializer_class = SafetyIncidentSourceSerializer

class SafetyIncidentFilter(django_filters.FilterSet):
    """
    source is a ForeignKey in SafetyIncident. We look it up by "name" in the query string.
    """
    source = django_filters.MethodFilter(action = lambda queryset, value: queryset.filter(source = SafetyIncidentSource.objects.filter(name = value)))
    location = django_filters.CharFilter(name="location",lookup_type="icontains")
    type = django_filters.CharFilter(name="type",lookup_type="icontains")

    class Meta:
        model = SafetyIncident
        fields = ('source', 'location', 'type')

class SafetyIncidentViewSet(viewsets.ModelViewSet):
    queryset = SafetyIncident.objects.all()
    serializer_class = SafetyIncidentSerializer
    filter_class = SafetyIncidentFilter

class SafetyIncidentAlertViewSet(viewsets.ModelViewSet):
    queryset = SafetyIncidentAlert.objects.all()
    serializer_class = SafetyIncidentAlertSerializer

class SafetyIncidentAlertBoundaryViewSet(viewsets.ModelViewSet):
    queryset = SafetyIncidentAlertBoundary.objects.all()
    serializer_class = SafetyIncidentAlertBoundarySerializer


from dataview.models import Attribute, Node
from api.serializers import AttributeSerializer, NodeSerializer


class AttributeFilter(django_filters.FilterSet):
    node = django_filters.MethodFilter(action = lambda queryset, value: queryset.filter(node = Node.objects.filter(name = value)))

    class Meta:
        model = Attribute
        fields = ('node', 'name')


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_class = AttributeFilter
