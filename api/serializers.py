from django.contrib.auth.models import User, Group
from rest_framework import serializers

from portal.models import Address, Destination, Guest, Message, OpenHour, Residence, Room

from sensors.models import Sensor
from security.models import SafetyIncident
from sign.models import Sign

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')  

# portal serializers
class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'city')

class OpenHourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OpenHour
        fields = ('from_hour', 'to_hour', 'day_of_week', 'location')
        
class DestinationSerializer(serializers.HyperlinkedModelSerializer):
    #open_hours = OpenHourSerializer(source='location')
    class Meta:
        model = Destination
        fields = ('title', 'location', 'open_hours')

class GuestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guest
        fields = ['name']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('location', 'subject', 'message')
        
class ResidenceSerializer(serializers.HyperlinkedModelSerializer):
    tenants = serializers.HyperlinkedRelatedField(many = True, read_only = True, view_name = 'user-detail', lookup_field = 'username')

    class Meta:
        model = Residence
        fields = ('name', 'location', 'floors', 'residence_floor', 'year', 'rent', 'tenants')

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'location')

# sensor serializers
class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensor
        fields = ('name', 'location')

# security serializers
class SafetyIncidentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SafetyIncident
        fields = ('location', 'units', 'type')

# sign serializers
class SignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sign
        fields = ('name', 'location', 'background_image')