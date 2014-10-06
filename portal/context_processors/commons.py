from portal.models import Message, Residence

def add_commons(request):
    d = {}
    if request.user.is_authenticated():
        d =  {'portal_messages': Message.objects.filter(user=request.user, acknowledged=False),
                'portal_residences': Residence.objects.filter(tenants=request.user)}
    return d