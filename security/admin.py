from django.contrib import admin
from security.models import Camera, SafetyIncident

class CameraAdmin(admin.ModelAdmin):
    list_display = ('location', 'residence')
    pass

admin.site.register(Camera, CameraAdmin)

class SafetyIncidentAdmin(admin.ModelAdmin):
    list_display = ('location', 'type')
    pass

admin.site.register(SafetyIncident, SafetyIncidentAdmin)