from django.conf import settings
from django.db.models import Q

from django.contrib.auth.models import Permission
from portal.models import Message, Residence

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
              'portal_residences': Residence.objects.filter(tenants=request.user),
              'portal_apps': apps}
    return d