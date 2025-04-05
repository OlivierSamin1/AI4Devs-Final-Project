import logging
from django.contrib import admin
from django import forms
import datetime
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .models import (
    Asset,
    CoproManagementCompany,
    CoproManagementContract,
    Mortgage,
    RentingManagementCompany,
    RentingManagementContract,
    UtilityContract,
    UtilitySupplier,
    Tenant,
    Bill,
    HollydaysPlatform,
    HollydaysReservation,
    FileBill,
    FileMortgage,
    FileRenting,
    FileTenant,
    FileAsset,
    FileCoPro,
    FileUtility,
    FileHollyDaysPlatform,
    FileHollyDaysReservation,
)
from .actions import (
    Results,
    Photo,
    PriceBill,
    PriceRent,
    # generate_report,
    AssetCsv,
    BillFiles,
    BillRent,
    SumAllDaysRented,
    BillsCsvDetailed,
)

logger = logging.getLogger(__name__)


def get_year_data_for_renting_admin(modeladmin, request, queryset):
    data = Results().handle(request)
    instance = queryset.first()
    instance.annual_results[list(data.keys())[0]] = list(data.values())[0]
    instance.save()
get_year_data_for_renting_admin.short_description = 'get year results and details - take 30 seconds'


def generate_csv_asset(modeladmin, request, queryset):
    logger.info("Action started.")
    logger.info("Request: %s", request)
    logger.info("Queryset: %s", queryset)
    AssetCsv().handle(request, queryset)
    # generate_csv(request, queryset)
generate_csv_asset.short_description = 'generate a csv with all income and outcome for the selected assets'


def get_bill_files(modeladmin, request, queryset):
    BillFiles().handle(request, queryset)
get_bill_files.short_description = 'get the bill files in a zip'


def get_bill_csv_details(modeladmin, request, queryset):
    BillsCsvDetailed().handle(request, queryset)
get_bill_csv_details.short_description = 'get the csv of the bills details'


def get_bill_summary(modeladmin, request, queryset):
    prices = PriceBill().handle(request, queryset)
get_bill_summary.short_description = 'get the bill prices and sum'


def get_rentings_total(modeladmin, request, queryset):
    prices = PriceRent().handle(request, queryset)
get_rentings_total.short_description = 'get the total income of selected rents'


def calculate_all_days(modeladmin, request, queryset):
    SumAllDaysRented().handle(request, queryset)
calculate_all_days.short_description = 'return the total number of days occupied by year of select reservations'


def generate_bill_rent_pdf(modeladmin, request, queryset):
    BillRent().handle(request, queryset)
    generate_bill_rent_pdf.short_description = 'generate a zip files with renting bills' \



class LastMonthFilter(SimpleListFilter):
    title = _('Last Month')
    parameter_name = 'last_month'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Last Month')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            today = datetime.date.today()
            last_month_end = today.replace(day=1) - datetime.timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            return queryset.filter(entry_date__range=[last_month_start, last_month_end])


class FilesInlineAsset(admin.StackedInline):
    model = FileAsset
    extra = 0


class FilesInlineHollydaysPlatform(admin.StackedInline):
    model = FileHollyDaysPlatform
    extra = 0


class FilesInlineHollydaysReservation(admin.StackedInline):
    model = FileHollyDaysReservation
    extra = 2


class FilesInlineBill(admin.StackedInline):
    model = FileBill
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Set default value for the 'name' field
        for field_name, field in formset.form.base_fields.items():
            if field_name == 'name':  # Check if the field is 'name'
                field.initial = 'bill'
        return formset


class FilesInlineCoPro(admin.StackedInline):
    model = FileCoPro
    extra = 0


class FilesInlineMortgage(admin.StackedInline):
    model = FileMortgage
    extra = 0


class FilesInlineRenting(admin.StackedInline):
    model = FileRenting
    extra = 0


class FilesInlineUtility(admin.StackedInline):
    model = FileUtility
    extra = 0


class FilesInlineTenant(admin.StackedInline):
    model = FileTenant
    extra = 0


class AssetAdmin(admin.ModelAdmin):
    search_fields = ['owner__username', 'nickname', 'city']
    list_display = ('owner', 'nickname', 'city', 'buying_price', 'has_on_going_mortgage')
    list_filter = list_display
    actions = [get_year_data_for_renting_admin, generate_csv_asset]
    inlines = [FilesInlineAsset]


class CoproCompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'site_app_company']
    list_display = ('name', 'site_app_company')
    list_filter = list_display


class CoproContractAdmin(admin.ModelAdmin):
    search_fields = ['company', 'is_management_active']
    list_display = ('company', 'is_management_active')
    list_filter = list_display
    inlines = [FilesInlineCoPro]


class MortgageAdmin(admin.ModelAdmin):
    search_fields = ['asset', 'name']
    list_display = ('asset', 'name')
    list_filter = list_display
    inlines = [FilesInlineMortgage]


class RentingCompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'site_app_company']
    list_display = ('name', 'site_app_company')
    list_filter = list_display


class RentingContractAdmin(admin.ModelAdmin):
    search_fields = ['company']
    list_display = ('company',)
    list_filter = list_display
    inlines = [FilesInlineRenting]


class UtilitySupplierAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    list_filter = list_display


class UtilityContractAdmin(admin.ModelAdmin):
    search_fields = ['asset', 'service', 'user', 'supplier', 'is_active', 'monthly_price']
    list_display = ('asset', 'service', 'user', 'supplier', 'is_active', 'monthly_price')
    # list_display = [field.name for field in UtilityContract._meta.get_fields()]
    list_filter = list_display
    inlines = [FilesInlineUtility]
    widgets = {'comments': forms.Textarea(attrs={'rows': 10, 'cols': 40})}


class TenantAdmin(admin.ModelAdmin):
    search_fields = ['asset', 'last_name', 'first_name', 'is_actual_tenant']
    list_display = ('is_actual_tenant', 'asset', 'last_name', 'first_name')
    list_filter = list_display
    inlines = [FilesInlineTenant]


class BillAdmin(admin.ModelAdmin):
    search_fields = ['asset__nickname', 'client_name__username', 'bill_name']
    list_display = ('asset', 'bill_name', 'date', 'total_price', 'bill_comment')
    list_filter = ('asset',)
    fields = ('asset', 'is_tax_deductible', 'client_name', "is_location_commission_bill", 'bill_name', 'bill_comment', 'date', 'total_price', 'tax', 'price_without_tax')
    actions = [get_bill_files, get_bill_summary, get_bill_csv_details]
    inlines = [FilesInlineBill]

    # Override the date_hierarchy to provide custom choices
    date_hierarchy = 'date'
    date_hierarchy_template = "admin/filter_date.html"  # Use the default template

    def changelist_view(self, request, extra_context=None):
        # Add the custom "Last Month" choice to the date hierarchy filter
        if extra_context is None:
            extra_context = {}
        extra_context['date_hierarchy_choices'] = [
            ('', '---------'),
            ('-30', 'Last Month'),  # Add the custom choice
        ]
        return super().changelist_view(request, extra_context=extra_context)



class HollydaysPlatformAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name',)
    list_filter = list_display
    fields = ('name', 'personal_email_used', 'site_app_company', 'comments')
    inlines = [FilesInlineHollydaysPlatform]


class HollydaysReservationAdmin(admin.ModelAdmin):
    search_fields = ['renting_person_full_name']
    list_display = ('platform', 'asset', 'renting_person_full_name',  'entry_date', 'end_date', 'price')
    list_filter = ('platform', 'asset')
    fields = ('platform', 'asset', 'price', 'received_bank', 'renting_person_full_name', 'renting_person_dni', 'renting_person_direction', 'renting_person_postcode', 'renting_person_city', 'renting_person_region', 'renting_person_country', 'entry_date', 'end_date', 'number_of_nights', 'cleaning', 'commission_platform', 'commission_other', 'comments')
    inlines = [FilesInlineHollydaysReservation]
    actions = [generate_bill_rent_pdf, get_rentings_total, calculate_all_days]
    widgets = {'comments': forms.Textarea(attrs={'rows': 10, 'cols': 40})}

    # Override the date_hierarchy to provide custom choices
    date_hierarchy = 'entry_date'
    date_hierarchy_template = "admin/filter_date.html"  # Use the default template



admin.site.register(HollydaysPlatform, HollydaysPlatformAdmin)
admin.site.register(HollydaysReservation, HollydaysReservationAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(UtilitySupplier, UtilitySupplierAdmin)
admin.site.register(UtilityContract, UtilityContractAdmin)
admin.site.register(CoproManagementCompany, CoproCompanyAdmin)
admin.site.register(CoproManagementContract, CoproContractAdmin)
admin.site.register(RentingManagementCompany, RentingCompanyAdmin)
admin.site.register(RentingManagementContract, RentingContractAdmin)
admin.site.register(Mortgage, MortgageAdmin)
admin.site.register(Tenant, TenantAdmin)
