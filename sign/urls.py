from django.conf.urls import include, url
from sign import views

urlpatterns = [
    url(r'^sign/(?P<id>[0-9a-f\-]+)$', views.sign, name='sign'),
    url(r'^sign/(?P<id>[0-9a-f\-]+)/dashing$', views.sign_dashing, name='sign_dashing'),
    url(r'^sign/(?P<id>[0-9a-f\-]+)/config$', views.sign_config, name='sign_config'),
    url(r'^sign/(?P<id>[0-9a-f\-]+)/widget/(?P<widget_id>[0-9a-f\-]+)$', views.sign_widget, name='sign_widget'),
]
