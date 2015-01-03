#from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import AddressSerializer, ResidenceSerializer, RoomSerializer, SensorSerializer, SignSerializer

from portal.models import Address, Residence, Room

# portal models

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ResidenceViewSet(viewsets.ModelViewSet):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer

    def list(self, request):
        queryset = Residence.objects.filter(tenants=request.user)
        serializer = ResidenceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    
# other applications

from sensors.models import Sensor

from sign.models import Sign

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SignViewSet(viewsets.ModelViewSet):
    queryset = Sign.objects.all()
    serializer_class = SignSerializer
