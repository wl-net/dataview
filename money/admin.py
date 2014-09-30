from django.contrib import admin
from money.models import Budget

class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Budget, BudgetAdmin)
