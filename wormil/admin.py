from django.contrib import admin
from .models import Fossil, Locality
from projects.admin import PaleoCoreLocalityAdminGoogle, PaleoCoreOccurrenceAdmin
from django import forms


@admin.register(Locality)
class LocalityAdmin(PaleoCoreLocalityAdminGoogle):
    list_display = ['locality_id', 'collection_code', 'name',
                    'earliest_age_ma', 'latest_age_ma', 'age_protocol', 'year_established',
                    'archaeological_evidence', 'archaeology_present',
                    'macrobotanical_evidence', 'macrobotanical_present',
                    'uncollected_taxa', 'uncollected_fossils_present']
    list_filter = ['collection_code', 'year_established', 'archaeology_present',
                   'macrobotanical_present', 'uncollected_fossils_present']
    search_fields = ['locality_id', 'name', 'bed']


@admin.register(Fossil)
class FossilAdmin(PaleoCoreOccurrenceAdmin):
    list_display = ['id', 'catalog_number', 'locality', 'found_by', 'recorded_by', 'description']
    readonly_fields = ['latitude', 'longitude']
    list_filter = ['collection_code', 'recorded_by', 'in_situ', 'matrix_adhering']
    search_fields = ['catalog_number', 'description', 'scientific_name', 'collector']
    list_display_links = ['id', 'catalog_number']





