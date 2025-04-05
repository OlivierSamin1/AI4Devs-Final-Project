from django.contrib import admin
from transportation.models.asset import Asset
from transportation.models.files import File


class FilesInline(admin.StackedInline):
    model = File
    extra = 0

class AssetAdmin(admin.ModelAdmin):
    search_fields = ['type', 'brand', 'model']
    list_display = ('type', 'brand', 'model')
    list_filter = list_display
    inlines = [FilesInline]


admin.site.register(Asset, AssetAdmin)
