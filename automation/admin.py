from django.contrib import admin
from automation.models import Automator, Controller, Decider, Task, TaskGroup


class AutomatorAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Automator, AutomatorAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Task, TaskAdmin)


class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(TaskGroup, TaskGroupAdmin)


class DeciderAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Decider, DeciderAdmin)


class ControllerAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Controller, ControllerAdmin)
