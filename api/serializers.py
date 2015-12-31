from django.contrib.auth.models import User
from rest_framework import serializers

from building.models import Address
from portal.models import Guest, Message

from sensors.models import Sensor, SensorValue
from security.models import Camera, SafetyIncidentSource, SafetyIncident, SafetyIncidentAlert, SafetyIncidentAlertBoundary
from sign.models import Sign
from transportation.models import Destination, OpenHour

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
        fields = ('name', 'location')

class GuestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guest
        fields = ['name']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('location', 'time', 'acknowledged', 'subject', 'message')

# sensor serializers
class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensor
        fields = ('name', 'location')

class SensorValueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SensorValue
        fields = ('sensor', 'updated', 'value')

# security serializers

class CameraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Camera
        fields = ('location', 'residence')

class SafetyIncidentSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SafetyIncidentSource
        fields = ['name']

class SafetyIncidentAlertBoundarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SafetyIncidentAlertBoundary
        fields = ['name']

class SafetyIncidentSerializer(serializers.HyperlinkedModelSerializer):
    source = serializers.SlugRelatedField(queryset = SafetyIncidentSource.objects.all(), read_only = False, slug_field = 'name')

    class Meta:
        model = SafetyIncident
        fields = ('source', 'location', 'time', 'units', 'type')

class SafetyIncidentAlertSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SafetyIncidentAlert
        fields = ('boundary', 'incident')

# sign serializers
class SignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sign
        fields = ('name', 'location', 'background_image')