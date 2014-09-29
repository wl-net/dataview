from django.contrib import admin
from portal.models import Address, Amenity, Neighbor, Destination, Employer, Bank, Residence, OpenHour

class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'zip')
    pass

admin.site.register(Address, AddressAdmin)

class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'reserverable')
    pass

admin.site.register(Amenity, AmenityAdmin)

class NeighborAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Neighbor, NeighborAdmin)

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location')
    pass

admin.site.register(Destination, DestinationAdmin)

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Employer, EmployerAdmin)

class BankAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Bank, BankAdmin)

class ResidenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Residence, ResidenceAdmin)


class OpenHourAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'location', 'from_hour', 'to_hour')
    save_as = True
    pass

admin.site.register(OpenHour, OpenHourAdmin)