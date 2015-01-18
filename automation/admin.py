from django.contrib import admin
from automation.models import Light, Speaker, SpeakerSourceController, Mood, RadioStation

class LightAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Light, LightAdmin)

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Speaker, SpeakerAdmin)

class SpeakerSourceControllerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(SpeakerSourceController, SpeakerSourceControllerAdmin)

class MoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled')
    pass

admin.site.register(Mood, MoodAdmin)

class RadioStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    pass

admin.site.register(RadioStation, RadioStationAdmin)