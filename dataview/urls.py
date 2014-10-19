from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

admin.site.site_header = "WLNet DataView Administrator"
admin.site.site_title = "WLNet DataView"

urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='index'),
    
    # app specific includes
    url(r'^portal/', include('portal.urls')),
    url(r'^sign/', include('sign.urls')),
    url(r'^transportation/', include('transportation.urls')),

    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
