from django.contrib import admin
from .models import HealthSymptom

@admin.register(HealthSymptom)
class HealthSymptomAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity', 'created_at')
    list_filter = ('severity',)
    search_fields = ('name', 'description') 