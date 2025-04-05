from django.contrib import admin
# from .actions import BillFromBankAccount
from .models import (
    BankAccount,
    BankCard,
    Bank,
    FileCard,
    FileAccount,
    BankAccountReport,
    FileAccountReport,
)


# def create_bill_instances(modeladmin, request, queryset):
#     BillFromBankAccount().handle(request, queryset)
# create_bill_instances.short_description = 'create bill instances from selected bank account monthly reports'


class FilesInlineCard(admin.StackedInline):
    model = FileCard
    extra = 0


class FilesInlineAccount(admin.StackedInline):
    model = FileAccount
    extra = 0


class FilesInlineAccountReport(admin.StackedInline):
    model = FileAccountReport
    extra = 0


class BankAccountAdmin(admin.ModelAdmin):
    search_fields = ['bank', 'name', 'IBAN', 'titular','is_account_open']
    list_display = ('name', 'bank', 'titular', 'IBAN', 'is_account_open')
    list_filter = ('name', 'titular', 'bank', 'is_account_open')
    inlines = [FilesInlineAccount]


class BankCardAdmin(admin.ModelAdmin):
    search_fields = ['bank_acount', 'name', 'is_active']
    list_display = ('name', 'is_active', 'bank_account', 'ending_date')
    list_filter = list_display
    inlines = [FilesInlineCard]


class BankAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    list_filter = list_display


class BankAccountReportAdmin(admin.ModelAdmin):
    search_fields = ['bank_account', 'date']
    list_display = ('bank_account', 'date')
    list_filter = ('bank_account', 'date')
    inlines = [FilesInlineAccountReport]
    # actions = [create_bill_instances]


admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(BankCard, BankCardAdmin)
admin.site.register(BankAccountReport, BankAccountReportAdmin)


