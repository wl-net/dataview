from django.contrib import admin
from automation.models import Automator, Decider, Controller, Task

class AutomatorAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Automator, AutomatorAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Task, TaskAdmin)

class DeciderAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Decider, DeciderAdmin)

class ControllerAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Controller, ControllerAdmin)
