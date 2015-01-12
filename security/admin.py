from django.contrib import admin
from security.models import Camera, SafetyIncidentSource, SafetyIncident

class CameraAdmin(admin.ModelAdmin):
    list_display = ('location', 'residence')
    pass

admin.site.register(Camera, CameraAdmin)


class SafetyIncidentSourceAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(SafetyIncidentSource, SafetyIncidentSourceAdmin)

class SafetyIncidentAdmin(admin.ModelAdmin):
    list_display = ('source', 'location', 'type', 'units')
    pass

admin.site.register(SafetyIncident, SafetyIncidentAdmin)