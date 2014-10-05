from django.contrib import admin
from sensors.models import SensorType, Sensor

class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(SensorType, SensorTypeAdmin)

class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Sensor, SensorAdmin)
