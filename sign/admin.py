from django.contrib import admin
from sign.models import Sign, Widget, SignWidget

class SignAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    save_as = True
    pass

admin.site.register(Sign, SignAdmin)

class WidgetAdmin(admin.ModelAdmin):
    list_display = ['name']
    save_as = True
    pass

admin.site.register(Widget, WidgetAdmin)

class SignWidgetAdmin(admin.ModelAdmin):
    list_display = ('sign', 'widget')
    save_as = True
    pass

admin.site.register(SignWidget, SignWidgetAdmin)