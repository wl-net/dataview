from django.contrib import admin
from sign.models import Sign

class SignAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(Sign, SignAdmin)
