from django.contrib import admin
from transportation.models import Destination, DestinationGroup, OpenHour
from django.forms import SelectMultiple
from django.db import models

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(DestinationAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user;
        obj.save()

admin.site.register(Destination, DestinationAdmin)

class DestinationGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    formfield_overrides = { models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'10'})}, }
    pass

admin.site.register(DestinationGroup, DestinationGroupAdmin)

class OpenHourAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'location', 'from_time', 'to_time')
    save_as = True
    pass

admin.site.register(OpenHour, OpenHourAdmin)