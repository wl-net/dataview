from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'user', views.UserViewSet)

# portal routes
portal_router = routers.DefaultRouter()

portal_router.register(r'address', views.AddressViewSet)
portal_router.register(r'destination', views.DestinationViewSet)
portal_router.register(r'guest', views.GuestViewSet)
portal_router.register(r'message', views.MessageViewSet)
portal_router.register(r'openhour', views.OpenHourViewSet)
portal_router.register(r'residence', views.ResidenceViewSet)
portal_router.register(r'room', views.RoomViewSet)

# sensor routes
router.register(r'sensor', views.SensorViewSet)

# sign routes
router.register(r'sign', views.SignViewSet)
urlpatterns = [
    url(r'^1/', include(router.urls)),
    url(r'^1/portal/', include(portal_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]