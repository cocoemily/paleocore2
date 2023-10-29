# Django imports
from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.forms import TextInput, Textarea  # import custom form widgets

# Third party imports
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mapwidgets.widgets import GooglePointFieldWidget

# App imports
from sermar.models import Locality, Collection, Biology, Morphotype


# Admin Classes
class LocalityAdmin(admin.ModelAdmin):
    list_display = ['roost_id', 'landmark', 'priority', 'in_park', 'pellets', 'bones', 'analysis',
                    'owl_species', 'pellet_species', 'verbatim_roost_type', 'accumulating_agent', 'protected_area']
    list_filter = ['pellets', 'bones', 'analysis', 'accumulating_agent', 'protected_area']
    readonly_fields = ['easting', 'northing', 'longitude', 'latitude']
    search_fields = ['landmark', 'accumulating_agent', 'roost_id', 'roost_type']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '25'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    fieldsets = [
        ('Record Details', {
            'fields': [('roost_id', 'name'),
                       ('date_created', 'date_last_modified'),
                       ('problem',),
                       ('problem_comment',)]
        }),
        ('Item Details', {
            'fields': [('landmark',),
                       ('priority', 'sample_size',),
                       ('adequate_sample',),
                       ('in_park', 'protected_area'),
                       ('owls', 'owl_species'),
                       ('pellets', 'pellet_species'),
                       ('bones',),
                       ('roost_type',),
                       ('accumulating_agent',),
                       ('analysis',)]
        }),
        ('Verbatim Details', {
            'fields': [('verbatim_in_park',),
                       ('verbatim_analysis',),
                       ('verbatim_pellets',),
                       ('verbatim_bones',),
                       ('verbatim_roost_type',),
                       ('verbatim_easting', 'verbatim_northing', 'verbatim_utm_zone'),
                       ]
        }),
        ('Location Details', {
            'fields': [('longitude', 'latitude'),
                       ('easting', 'northing',),
                       ('geom',)]
        }),
    ]


class CollectionResource(resources.ModelResource):

    class Meta:
        model = Collection


class CollectionAdmin(ImportExportModelAdmin):
    readonly_fields = ['label']
    list_display = ['name','label', 'collection_code', 'locality', 'date', 'disposition', 'specimen_loc', 'sample_size',
                    'source', 'status', 'bags']
    list_filter = ['source', 'specimen_loc', 'locality']
    search_fields = ['collection_code', 'locality__name', 'locality__roost_id']

    resource_class = CollectionResource


class BiologyResource(resources.ModelResource):

    class Meta:
        model = Biology


class BiologyAdmin(ImportExportModelAdmin):
    list_display = ['barcode', 'collection', 'morphotype', 'element_id',  'loan', 'disposition', 'default_image']
    list_filter = ['collection_code', 'loan', 'verbatim_morphotype_id']
    search_fields = ['barcode', 'item_number']
    readonly_fields = ['default_image']
    fieldsets = [
        ('Record Details', {
            'fields': [
                ('barcode', 'field_number_orig'),
                ('morphobank_number',),
                ('basis_of_record', 'item_type'),
                ('collection',),
                ('collection_code', 'item_number', 'item_part'),
                ('related_catalog_items',),
                ('collector', 'finder'),
                ('loan', 'loan_date'),
                ('disposition',),
                ('individual_count',),
                ('preparation_status',),

            ]
        }),
        ('Identification', {
            'fields': [
                ('verbatim_morphotype_id', 'morphotype'),
                ('item_scientific_name', 'author_year_of_scientific_name'),
                ('infraspecific_epithet', 'infraspecific_rank'),
                ('nomenclatural_code',),
                ('identified_by', 'date_identified'),
                ('type_status',)
            ]
        }),
        ('Biology Details', {
            'fields': [
                ('sex',),
                ('life_stage',),
            ]
        }),
        ('Preservation', {
            'fields': [
                ('item_description',),
                ('side',),
                ('attributes',),
                ('collecting_method',),
                ('preparations',),
                ('in_situ',),
                ('weathering', 'surface_modification')
            ]
        }),
        ('Anatomical Elements', {
            'fields': [
                ('tooth_upper_or_lower',),
                ('tooth_number',),
                ('tooth_type',),
                ('element_id','element', 'element_modifier'),
                ('lli1', 'lri1', 'uri1', 'uli1'),
                ('lli2', 'lri2', 'uri2', 'uli2'),
                ('lli3', 'lri3', 'uri3', 'uli3'),
                ('lli4', 'lri4', 'uri4', 'uli4'),
                ('lli5', 'lri5', 'uri5', 'uli5'),
                ('llc', 'lrc', 'urc', 'ulc'),
                ('llp1', 'lrp1', 'urp1', 'ulp1'),
                ('llp2', 'lrp2', 'urp2', 'ulp2'),
                ('llp3', 'lrp3', 'urp3', 'ulp3'),
                ('llp4', 'lrp4', 'urp4', 'ulp4'),
                ('llm1', 'lrm1', 'urm1', 'ulm1'),
                ('llm2', 'lrm2', 'urm2', 'ulm2'),
                ('llm3', 'lrm3', 'urm3', 'ulm3'),

            ]
        }),
        ('Measurements', {
            'fields': [
                ('lm_tooth_row_length_mm',),
                ('lm_1_length', 'lm_1_width'),
                ('lm_2_length', 'lm_2_width'),
                ('lm_3_length', 'lm_3_width'),
                ('um_tooth_row_length_mm',),
                ('um_1_length_mm', 'um_1_width_mm'),
                ('um_2_length_mm', 'um_2_width_mm'),
                ('um_3_length_mm', 'um_3_width_mm'),
            ]
        }),
        ('Remarks', {
            'fields': [
                ('fauna_notes',),
                ('remarks',),
                ('problem',),
                ('problem_comment',),
                ('date_created', 'date_last_modified'),

            ]
        }),

    ]

    resource_class = BiologyResource

class MorphotypeAdmin(admin.ModelAdmin):
    list_display = ['morph_id', 'name', 'order_id', 'species1_id', 'species2_id', 'species3_id', 'species4_id',
                    'analysis_id']
    list_filter = ['order_id']
    search_fields = ['name', 'morph_id']

# Admin Registration
admin.site.register(Biology, BiologyAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Morphotype, MorphotypeAdmin)
