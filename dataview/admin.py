from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from dataview.models import SystemDeployment

class SystemDeploymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    pass

admin.site.register(SystemDeployment, SystemDeploymentAdmin)

class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('WLNet DataView')

    # Text to put in each page's <h1>.
    site_header = ugettext_lazy('My administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('DataView administration')
    
admin_site = MyAdminSite()
