from django.contrib import admin
from django.contrib.admin import SimpleListFilter
import datetime
from django.utils.translation import gettext_lazy as _
from .models import (
    Bill,
    FileBill,
    FileProduct,
    FileSymptom,
    Product,
    Symptom,
)


class FilesInlineBill(admin.StackedInline):
    model = FileBill
    extra = 0


class FilesProductInlineBill(admin.StackedInline):
    model = FileProduct
    extra = 0

class FilesSymptomInlineBill(admin.StackedInline):
    model = FileSymptom
    extra = 0


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


class BillAdmin(admin.ModelAdmin):
    search_fields = ['client_name__username', 'bill_name']
    list_display = ('client_name', 'bill_name', 'date', 'total_price', 'is_paid', 'is_asked_by_us')
    list_filter = ('client_name', 'date', 'bill_name', 'total_price', 'is_paid', 'is_asked_by_us')
    fields = ('client_name', 'bill_name', 'date', 'total_price', 'is_paid', 'is_asked_by_us')

    # Override the date_hierarchy to provide custom choices
    date_hierarchy = 'date'
    date_hierarchy_template = "admin/filter_date.html"  # Use the default template
    inlines = [FilesInlineBill]


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'natural', 'child_use', 'adult_use', 'min_age']
    list_display = ('name', 'natural', 'child_use', 'adult_use', 'min_age')
    list_filter = ('name', 'natural', 'child_use', 'adult_use', 'min_age')
    fields = ('name', 'natural', 'child_use', 'adult_use', 'min_age', 'source_info', 'date_info', 'composition', 'interests', 'comments')
    inlines = [FilesProductInlineBill]


class SymptomAdmin(admin.ModelAdmin):
    search_fields = ['name', 'child', 'adult']
    list_display = ('name', 'child', 'adult')
    list_filter = ('name', 'child', 'adult')
    fields = ('name', 'child', 'adult', 'products', 'comments')
    inlines = [FilesSymptomInlineBill]


admin.site.register(Bill, BillAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Symptom, SymptomAdmin)
