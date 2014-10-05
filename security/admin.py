from django.contrib import admin
from security.models import Camera

class CameraAdmin(admin.ModelAdmin):
    list_display = ('location', 'residence')
    pass

admin.site.register(Camera, CameraAdmin)