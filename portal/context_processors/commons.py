from django.conf import settings
from django.db.models import Q

from django.contrib.auth.models import User,Permission
from portal.models import Message

def add_commons(request):
    d = {}
    if request.user.is_authenticated():
        """
        TODO: clean this up. Create tests first
        """
        permissions = []
        for permission in Permission.objects.filter(Q(user=request.user) | Q(group__user=request.user)):
            if permission.content_type.app_label not in permissions:
                permissions.append(permission.content_type.app_label)
        apps = []
        for app in sorted(settings.DATAVIEW_APPS):
            if app in permissions:
                apps.append(app)

        d =  {'portal_messages': Message.objects.filter(user=request.user, acknowledged=False),
              'portal_apps': apps,
              'portal_current_app': '',
              'portal_current_user': User.objects.get(username=request.user),
              }
    return d