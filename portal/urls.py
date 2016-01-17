from django.conf.urls import patterns, include, url
from django.conf import settings
from portal.views import index, dismiss_message

urlpatterns = [
    url(r'^portal/$', index, name='index'),
    url(r'^portal/api/dismiss-message', dismiss_message, name='dismiss_message'),
]

for app in settings.DATAVIEW_APPS:
    if app == 'portal':
        continue

    try:
        urlpatterns += [url('^portal/' + app, include(app + '.portal.urls'))]
    except ImportError as e:
        if "No module named '" + app + '.portal' +  "'" != str(e):

            import traceback
            print(traceback.format_exc())
