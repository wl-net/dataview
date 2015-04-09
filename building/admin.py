from django.contrib import admin, gis
from building.models import Address, Amenity, Building, Room

class AddressAdmin(gis.admin.OSMGeoAdmin):
    list_display = ('street', 'city', 'zip')
    pass

admin.site.register(Address, AddressAdmin)

class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'reserverable')
    pass

admin.site.register(Amenity, AmenityAdmin)

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    pass

admin.site.register(Building, BuildingAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'square_feet')
    pass

admin.site.register(Room, RoomAdmin)