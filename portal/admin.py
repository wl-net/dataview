from django.forms import SelectMultiple
from django.db import models
from django.contrib import admin, gis
from portal.models import Address, Amenity, Neighbor, Room, ServiceType, Service, Guest
from portal.models import TimeEntry, Employer, Residence

class AddressAdmin(gis.admin.OSMGeoAdmin):
    list_display = ('street', 'city', 'zip')
    pass

admin.site.register(Address, AddressAdmin)

class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'reserverable')
    pass

admin.site.register(Amenity, AmenityAdmin)

class NeighborAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'location')
    pass

admin.site.register(Neighbor, NeighborAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'square_feet')
    pass

admin.site.register(Room, RoomAdmin)

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

class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('start', 'end')
    pass

admin.site.register(TimeEntry, TimeEntryAdmin)

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Employer, EmployerAdmin)

class ResidenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Residence, ResidenceAdmin)
