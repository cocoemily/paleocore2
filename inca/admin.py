from django.contrib import admin
from .models import Specimen
from projects.admin import PaleoCoreOccurrenceAdmin


@admin.register(Specimen)
class FossilAdmin(PaleoCoreOccurrenceAdmin):
    list_display = ['id', 'catalog_number', 'found_by', 'recorded_by', 'description']
    readonly_fields = ['latitude', 'longitude']
    list_filter = ['collection_code', 'recorded_by', 'in_situ']
    search_fields = ['id', 'catalog_number', 'description', 'scientific_name', 'found_by__name']
    list_display_links = ['id', 'catalog_number']
