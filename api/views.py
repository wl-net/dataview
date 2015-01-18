from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.response import Response

from api.serializers import UserSerializer, AddressSerializer, DestinationSerializer, GuestSerializer, MessageSerializer, OpenHourSerializer, PackageSerializer
from api.serializers import ResidenceSerializer, RoomSerializer

from portal.models import Address, Destination, Guest, Message, OpenHour, Package, Residence, Room

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

import django_filters

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


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class ResidenceViewSet(viewsets.ModelViewSet):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer

    def list(self, request):
        queryset = Residence.objects.filter(tenants=request.user)
        serializer = ResidenceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.none()
    serializer_class = RoomSerializer

    def list(self, request):
        queryset = Room.objects.filter(location=Residence.objects.filter(tenants = request.user)) # critical
        serializer = RoomSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Room.objects.filter(location=Residence.objects.filter(tenants = request.user)) # critical
        room = get_object_or_404(queryset, pk=pk)
        serializer = RoomSerializer(room, context={'request': request})
        return Response(serializer.data)
    
# other applications

from sensors.models import Sensor
from api.serializers import SensorSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

# security application

from security.models import Camera, SafetyIncidentSource, SafetyIncident
from api.serializers import CameraSerializer, SafetyIncidentSourceSerializer, SafetyIncidentSerializer

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

# sign applications

from sign.models import Sign
from api.serializers import SignSerializer

class SignViewSet(viewsets.ModelViewSet):
    queryset = Sign.objects.all()
    serializer_class = SignSerializer