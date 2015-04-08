from django.contrib import admin
from automation.models import Automator, Decider, Controller

class AutomatorAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Automator, AutomatorAdmin)

class DeciderAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Decider, DeciderAdmin)

class ControllerAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Controller, ControllerAdmin)
