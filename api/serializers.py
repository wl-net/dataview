from django.contrib.auth.models import User, Group
from rest_framework import serializers

from portal.models import Address, Destination, Guest, Message, OpenHour, Package, Residence, Room

from sensors.models import Sensor
from security.models import SafetyIncidentSource, SafetyIncident
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

class PackageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Package
        fields = ('tracking_number', 'location', 'picked_up')


class DestinationSerializer(serializers.HyperlinkedModelSerializer):
    #open_hours = OpenHourSerializer(source='location')
    class Meta:
        model = Destination
        fields = ('name', 'location')

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

class SafetyIncidentSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SafetyIncidentSource
        fields = ['name']

class SafetyIncidentSerializer(serializers.HyperlinkedModelSerializer):
    source = serializers.SlugRelatedField(queryset = SafetyIncidentSource.objects.all(), read_only = False, slug_field = 'name')

    class Meta:
        model = SafetyIncident
        fields = ('source', 'location', 'time', 'units', 'type')

# sign serializers
class SignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sign
        fields = ('name', 'location', 'background_image')