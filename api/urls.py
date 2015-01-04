from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'user', views.UserViewSet)

# portal routes
router.register(r'address', views.AddressViewSet)
router.register(r'destination', views.DestinationViewSet)
router.register(r'openhour', views.OpenHourViewSet)
router.register(r'residence', views.ResidenceViewSet)
router.register(r'room', views.RoomViewSet)

# sensor routes
router.register(r'sensor', views.SensorViewSet)

# sign routes
router.register(r'sign', views.SignViewSet)

urlpatterns = [
    url(r'^1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]