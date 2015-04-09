from django.contrib import admin
from security.models import Camera, SafetyIncidentSource, SafetyIncidentAlertBoundary, SafetyIncident
import floppyforms as forms
from django.contrib.gis.db.models import MultiPolygonField

from django.contrib import gis 

class CameraAdmin(admin.ModelAdmin):
    list_display = ('location', 'residence')
    pass

admin.site.register(Camera, CameraAdmin)


class SafetyIncidentSourceAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(SafetyIncidentSource, SafetyIncidentSourceAdmin)

class SafetyIncidentAlertBoundaryAdmin(gis.admin.OSMGeoAdmin):
    list_display = ['name']
    ordering = ['name']

    pass

admin.site.register(SafetyIncidentAlertBoundary, SafetyIncidentAlertBoundaryAdmin)

class SafetyIncidentAdmin(admin.ModelAdmin):
    list_display = ('time', 'location', 'type', 'units', 'source')
    ordering = ('-time', 'location')
    pass

admin.site.register(SafetyIncident, SafetyIncidentAdmin)