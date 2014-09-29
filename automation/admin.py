from django.contrib import admin
from automation.models import Light, Mood, RadioStation

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