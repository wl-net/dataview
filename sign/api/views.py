from rest_framework import viewsets, filters

from sign.models import Sign
from api.serializers import SignSerializer

class SignViewSet(viewsets.ModelViewSet):
    queryset = Sign.objects.all()
    serializer_class = SignSerializer
