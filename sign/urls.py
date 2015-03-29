from django.conf.urls import patterns, include, url
from sign.api import urls

urlpatterns = patterns('',
    url(r'^sign/(?P<id>[0-9]+)$', 'sign.views.sign', name='sign'),
    url(r'^sign/(?P<id>[0-9]+)/dashing$', 'sign.views.sign_dashing', name='sign_dashing'),
    url(r'^sign/config/(?P<id>[0-9]+)$', 'sign.views.sign_config', name='sign_config'),
    url(r'^sign/(?P<id>[0-9]+)/widget/(?P<widget_id>[0-9]+)$', 'sign.views.sign_widget', name='sign_widget'),
)
