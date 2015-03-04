from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^portal/$', 'portal.views.index', name='index'),
    url(r'^portal/api/dismiss-message', 'portal.views.dismiss_message', name='dismiss_message'),
)

for app in settings.DATAVIEW_APPS:
    print(app)
    try:
      urlpatterns += patterns('', url('^portal/' + app, include(app + '.portal.urls')))
    except Exception:
        pass
