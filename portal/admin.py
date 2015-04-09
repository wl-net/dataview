from django.forms import SelectMultiple
from django.db import models
from django.contrib import admin, gis
from portal.models import Neighbor, ServiceType, Service, Guest
from portal.models import Residence


class NeighborAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'location')
    pass

admin.site.register(Neighbor, NeighborAdmin)

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(ServiceType, ServiceTypeAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Service, ServiceAdmin)

class GuestAdmin(admin.ModelAdmin):
    list_display = ['name']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user;
        obj.save()

admin.site.register(Guest, GuestAdmin)

class ResidenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Residence, ResidenceAdmin)
