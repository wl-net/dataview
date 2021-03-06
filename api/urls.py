from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

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

# sensor routes
router.register(r'sensor', views.SensorViewSet)
router.register(r'sensor-value', views.SensorValueViewSet)

# sign routes
#router.register(r'sign', views.SignViewSet)

# security routes
router.register(r'camera', views.CameraViewSet)
router.register(r'safety-incident-source', views.SafetyIncidentSourceViewSet)
router.register(r'safety-incident', views.SafetyIncidentViewSet)
router.register(r'safety-incident-alert', views.SafetyIncidentAlertViewSet)
router.register(r'safety-incident-alert-boundary', views.SafetyIncidentAlertBoundaryViewSet)

router.register(r'node-attributes', views.AttributeViewSet)

urlpatterns = [
    url(r'^1/', include(router.urls)),
    url(r'^1/portal/', include(portal_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get-auth-token', authtoken_views.obtain_auth_token),
]

for app in settings.DATAVIEW_APPS:
    try:
        urlpatterns += [url('^1/{}/'.format(app), include(app + '.api.urls'))]
    except ImportError as e:
        if "No module named '" + app + '.api' +  "'" != str(e):

            import traceback
            print(traceback.format_exc())
