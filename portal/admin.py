from django.contrib import admin
from portal.models import Address, Amenity, Destination, Light, Mood, RadioStation, Residence, OpenHour

class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'zip')
    pass

admin.site.register(Address, AddressAdmin)

class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'reserverable')
    pass

admin.site.register(Amenity, AmenityAdmin)

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location')
    pass

admin.site.register(Destination, DestinationAdmin)

class LightAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Light, LightAdmin)


class MoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled')
    pass

admin.site.register(Mood, MoodAdmin)

class RadioStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    pass

admin.site.register(RadioStation, RadioStationAdmin)

class ResidenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Residence, ResidenceAdmin)


class OpenHourAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'location', 'from_hour', 'to_hour')
    save_as = True
    pass

admin.site.register(OpenHour, OpenHourAdmin)