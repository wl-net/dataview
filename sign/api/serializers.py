from rest_framework import serializers

from sign.models import Sign

class SignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sign
        fields = ('name', 'location', 'background_image')