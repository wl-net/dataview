from django.conf.urls import url, include
from rest_framework import routers

from sign.api import views

router = routers.DefaultRouter()
router.register(r'sign', views.SignViewSet)

urlpatterns = [
    url(r'^1/', include(router.urls)),
]
