from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^portal/$', 'portal.views.index', name='index'),
    url(r'^portal/api/dismiss-message', 'portal.views.dismiss_message', name='dismiss_message'),
)

for app in settings.DATAVIEW_APPS:
    try:
        urlpatterns += patterns('', url('^portal/' + app, include(app + '.portal.urls')))
    except ImportError as e:
        if "No module named '" + app + '.portal' +  "'" != str(e):

            import traceback
            print(traceback.format_exc())
