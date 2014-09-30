from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='index'),

    # portal views
    url(r'^money$', 'portal.views.money', name='money'),
    url(r'^transportation$', 'portal.views.transportation', name='transportation'),
    url(r'^security', 'portal.views.security', name='security'),
    url(r'^automation', 'portal.views.automation', name='automation'),
    url(r'^news', 'portal.views.news', name='news'),
    url(r'^communication', 'portal.views.communication', name='communication'),
)
