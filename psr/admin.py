from django.contrib.gis import admin
from django.urls import reverse, path

from import_export import resources
import unicodecsv

from .models import *  # import database models from models.py
import projects.admin
from .views import ImportKMZ

psr_occurrence_fieldsets = (
    ('Record Details', {
        'fields': [('field_id', 'item_type', 'find_type', 'item_description'),
                   ('basis_of_record',),
                   ('remarks', 'date_created',),
                   ('date_last_modified')]
    }),  # lgrp_occurrence_fieldsets[0]
    ('Find Details', {
        'fields': [('collecting_method',),
                   ('collector', 'finder', 'item_count', 'field_number',),
                   ]
    }),  # lgrp_occurrence_fieldsets[1]
    ('Photos', {
        'fields': [('photo', 'image')],
        # 'classes': ['collapse'],
    }),  # lgrp_occurrence_fieldsets[2]  # lgrp_occurrence_fieldsets[3]
    ('Location', {
        'fields': [('geom',), ('point')]
    }),  # lgrp_occurrence_fieldsets[4]
    ('Problems', {
        'fields': [('problem', 'problem_comment'),
                   ],
        'classes': ['collapse']
    }),  # lgrp_occurrence_fieldsets[5]
)

psr_gc_fieldsets = (
    ('Record Details', {
        'fields': [('name', 'context_type',  ),
                   ('basis_of_record', 'collecting_method'),
                   ('remarks', 'date_created'),
                   ('date_last_modified')]
    }),  # lgrp_occurrence_fieldsets[0]
    ('Geology Details', {
        'fields': [('geology_type'), ('description'), ('dip', 'strike', 'color', 'texture', 'height', 'width', 'depth'),
                   ('slope_character'), ('sediment_presence', 'sediment_character', ),
                   ('cave_mouth_character'), ('rockfall_character'), ('speleothem_character')
                   ]
    }),  # lgrp_occurrence_fieldsets[1]
    ('Photos', {
        'fields': [('image')],
        # 'classes': ['collapse'],
    }),  # lgrp_occurrence_fieldsets[2]  # lgrp_occurrence_fieldsets[3]
    ('Location', {
        'fields': [('geom', 'point')]
    }),  # lgrp_occurrence_fieldsets[4]
    ('Problems', {
        'fields': [('problem', 'problem_comment'),
                   ],
        'classes': ['collapse']
    }),  # lgrp_occurrence_fieldsets[5]
)

class ImagesInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ("id",)


class FilesInline(admin.TabularInline):
    model = File
    extra = 0
    readonly_fields = ("id",)


# Define Occurrence resource class for django import-export
class OccurrenceResource(resources.ModelResource):
    class Meta:
        model = Occurrence


class OccurrenceAdmin(projects.admin.PaleoCoreOccurrenceAdmin):
    resource_class = OccurrenceResource
    #empty_value_display = '-empty-'

    default_read_only_fields = ('id', 'geom', 'point_x', 'point_y', 'easting', 'northing', 'date_last_modified', 'date_collected')
    readonly_fields = default_read_only_fields + ('photo', 'catalog_number', 'longitude', 'latitude')
    default_list_filter = [ 'item_type', 'basis_of_record', 'collector', 'finder']
    list_filter = default_list_filter
    search_fields = ['id', 'item_type', 'item_description', 'barcode', 'field_id']
    list_per_page = 500

    list_display = ('field_id', 'item_type', 'find_type', 'geological_context_id')
    fieldsets = psr_occurrence_fieldsets

    def get_urls(self):
        tool_item_urls = [
            path(r'import_kmz/', ImportKMZ.as_view()),
            # path(r'^summary/$',permission_required('mlp.change_occurrence',
            #                         login_url='login/')(self.views.Summary.as_view()),
            #     name="summary"),
        ]
        return tool_item_urls + super(OccurrenceAdmin, self).get_urls()


class GeologicalContextResource(resources.ModelResource):
    class Meta:
        model = GeologicalContext


class GeologicalContextAdmin(projects.admin.PaleoCoreOccurrenceAdmin):
    resource_class = GeologicalContextResource
    #empty_value_display = '-empty-'
    readonly_fields = ('id', 'geom', 'point_x', 'point_y', 'easting', 'northing', 'date_last_modified', 'date_collected')
    list_filter = ['context_type', 'basis_of_record', 'collecting_method', 'geology_type', 'sediment_presence']
    list_per_page = 500
    search_fields = ['id', 'item_scientific_name', 'item_description', 'barcode', 'cat_number']

    list_display = ('name', 'context_type', 'geology_type')
    fieldsets = psr_gc_fieldsets


class ArchaeologyResource(resources.ModelResource):
    class Meta:
        model = Archaeology


class ArchaeologyAdmin(OccurrenceAdmin):
    model = Archaeology
    resource_class = ArchaeologyResource
    #empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'archaeology_type')


class BiologyResource(resources.ModelResource):
    class Meta:
        model = Biology


class BiologyAdmin(OccurrenceAdmin):
    model = Archaeology
    resource_class = ArchaeologyResource
    #empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'biology_type')


class GeologyResource(resources.ModelResource):
    class Meta:
        model = Geology


class GeologyAdmin(OccurrenceAdmin):
    model = Geology
    resource_class = GeologyResource
    #empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'geology_type')


class AggregateResource(resources.ModelResource):
    class Meta:
        model = Aggregate


class AggregateAdmin(OccurrenceAdmin):
    model = Aggregate
    resource_class = AggregateResource
    #empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'screen_size')


admin.site.register(Biology, BiologyAdmin)
admin.site.register(Archaeology, ArchaeologyAdmin)
admin.site.register(Geology, GeologyAdmin)
admin.site.register(GeologicalContext, GeologicalContextAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(Taxon, projects.admin.TaxonomyAdmin)
admin.site.register(Aggregate, AggregateAdmin)
