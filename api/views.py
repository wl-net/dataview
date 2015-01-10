from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import UserSerializer, AddressSerializer, DestinationSerializer, GuestSerializer, MessageSerializer, OpenHourSerializer
from api.serializers import ResidenceSerializer, RoomSerializer, SensorSerializer, SafetyIncidentSerializer, SignSerializer

from portal.models import Address, Destination, Guest, Message, OpenHour, Residence, Room

class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer

# portal models

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

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

from security.models import SafetyIncident

from sign.models import Sign

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SafetyIncidentViewSet(viewsets.ModelViewSet):
    queryset = SafetyIncident.objects.all()
    serializer_class = SafetyIncidentSerializer

class SignViewSet(viewsets.ModelViewSet):
    queryset = Sign.objects.all()
    serializer_class = SignSerializer
