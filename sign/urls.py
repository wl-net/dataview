from django.conf.urls import patterns, include, url
from sign.api import urls

urlpatterns = patterns('',
    url(r'^sign/(?P<id>[0-9a-f\-]+)$', 'sign.views.sign', name='sign'),
    url(r'^sign/(?P<id>[0-9a-f\-]+)/dashing$', 'sign.views.sign_dashing', name='sign_dashing'),
    url(r'^sign/(?P<id>[0-9a-f\-]+)/config$', 'sign.views.sign_config', name='sign_config'),
    url(r'^sign/(?P<id>[0-9a-f\-]+)/widget/(?P<widget_id>[0-9a-f\-]+)$', 'sign.views.sign_widget', name='sign_widget'),
)
