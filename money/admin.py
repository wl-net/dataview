from django.contrib import admin
from money.models import Bank, Budget

class BankAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Bank, BankAdmin)

class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass

admin.site.register(Budget, BudgetAdmin)
