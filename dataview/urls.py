from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

admin.site.site_header = "WLNet DataView Administrator"
admin.site.site_title = "WLNet DataView"

urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='index'),

    # sign hacks
    url(r'^sign$', 'sign.views.index', name='index'),
    url(r'^sign/transit$', 'sign.views.transit', name='transit'),
    url(r'^sign/transit/destinations$', 'sign.views.destinations', name='destinations'),
   
    #url(r'^portal/transportation/mobile$', 'portal.views.transportation_mobile', name='transportation_mobile'),
    #url(r'^error$', 'sign.views.error', name='error'),
    
    # app specific includes
    url(r'^portal/', include('portal.urls')),

    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
