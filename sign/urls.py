from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<id>[0-9]+)$', 'sign.views.sign', name='sign'),
)
