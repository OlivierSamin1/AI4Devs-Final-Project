from django.contrib import admin
from .models import (
    Document,
    InsuranceContract,
    InsuranceCompany,
    FileDocument,
    FileInsuranceContract,
)


class FilesInlineDocument(admin.StackedInline):
    model = FileDocument
    extra = 0


class FilesInlineInsuranceContract(admin.StackedInline):
    model = FileInsuranceContract
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('user', 'type', 'name')
    list_filter = ('user', 'type')
    inlines = [FilesInlineDocument]


class InsuranceCompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'phone_number')
    list_filter = ('name', 'phone_number')


class InsuranceContractAdmin(admin.ModelAdmin):
    search_fields = ['company']
    list_display = ('company', 'type', 'is_insurance_active')
    list_filter = ('company', 'type', 'is_insurance_active')
    inlines = [FilesInlineInsuranceContract]


admin.site.register(Document, DocumentAdmin)
admin.site.register(InsuranceContract, InsuranceContractAdmin)
admin.site.register(InsuranceCompany, InsuranceCompanyAdmin)
