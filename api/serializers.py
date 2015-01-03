from django.contrib.auth.models import User, Group
from rest_framework import serializers

from portal.models import Address, Residence, Room

from sensors.models import Sensor
from sign.models import Sign

# portal serializers
class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'city')

class ResidenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Residence
        fields = ('name', 'location', 'floors', 'residence_floor', 'year')

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'location')

# sensor serializers
class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensor
        fields = ('name', 'location')

# sign serializers
class SignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sign
        fields = ('name', 'location', 'background_image')