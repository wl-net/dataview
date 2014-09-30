from portal.models import Message, Residence

def add_commons(request):
    return {'portal_messages': Message.objects.filter(user=request.user, acknowledged=False),
            'residences': Residence.objects.filter()}