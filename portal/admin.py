from django.contrib import admin
from portal.models import Address, Amenity, Neighbor, Room, ServiceType, Service, Guest
from portal.models import TimeEntry, Destination, Employer, Residence, OpenHour

class AddressAdmin(admin.ModelAdmin):
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

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(DestinationAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user;
        obj.save()

admin.site.register(Destination, DestinationAdmin)

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Employer, EmployerAdmin)

class ResidenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Residence, ResidenceAdmin)


class OpenHourAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'location', 'from_time', 'to_time')
    save_as = True
    pass

admin.site.register(OpenHour, OpenHourAdmin)