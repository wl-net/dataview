from django.conf.urls import include, url
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib import admin
admin.autodiscover()

admin.site.site_header = "WLNet DataView Administrator"
admin.site.site_title = "WLNet DataView"

from portal.views import index
from dataview.views import v1_config

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^api/1/config$', v1_config, name='v1_config'),
    url(r'^api/', include('api.urls')),

    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    
    url(r'^account/login/$', LoginView.as_view(template_name='registration/login.html')),
    url(r'^account/logout/$', LogoutView.as_view()),

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

]