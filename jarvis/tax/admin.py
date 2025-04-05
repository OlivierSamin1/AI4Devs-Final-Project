from django.contrib import admin
from .models import (
    Tax,
    TaxManagementCompany,
    TaxManagementContract,
    FileTax,
    FileTaxManagement,
)

class FilesInlineTax(admin.StackedInline):
    model = FileTax
    extra = 0


class FilesInlineTaxManagement(admin.StackedInline):
    model = FileTaxManagement
    extra = 0


class TaxContractAdmin(admin.ModelAdmin):
    search_fields = ['company', 'is_contract_active']
    list_display = ('company', 'is_contract_active', 'annual_price')
    list_filter = list_display
    inlines = [FilesInlineTaxManagement]


class TaxCompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    list_filter = list_display


class TaxAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',  'tax_type', 'year', 'real_estate_tax_type', 'person', 'real_estate_asset', 'transportation_asset')
    list_filter = ('person', 'year', 'tax_type', 'real_estate_asset', 'transportation_asset')
    inlines = [FilesInlineTax]



admin.site.register(TaxManagementContract, TaxContractAdmin)
admin.site.register(TaxManagementCompany, TaxCompanyAdmin)
admin.site.register(Tax, TaxAdmin)
