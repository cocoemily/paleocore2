from django.contrib.gis import admin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.urls import path

from .models import *
from .views import ImportKMZ
import unicodecsv
import projects.admin
from projects.admin import TaxonomyAdmin, TaxonRankAdmin
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportExportActionModelAdmin


###############
# Media Admin #
###############
class ImagesInline(admin.TabularInline):
    model = Image
    readonly_fields = ['id', 'thumbnail']
    fields = ['id', 'image', 'thumbnail', 'description']
    extra = 0


class FilesInline(admin.TabularInline):
    model = File
    extra = 0
    readonly_fields = ("id",)


###################
# Hydrology Admin #
###################
class HydrologyAdmin(admin.GeoModelAdmin):
    list_display = ("id", "size")
    search_fields = ("id",)
    list_filter = ("size",)

    options = {
        'layers': ['google.terrain']
    }


##################
# Locality Admin #
##################
locality_fieldsets = (
    ('Record Details', {
        'fields': [('id',)]
    }),
    ('Item Details', {
        'fields': [('collection_code', 'locality_number', 'sublocality')]
    }),

    ('Occurrence Details', {
        'fields': [('description',)]
    }),
    ('Geological Context', {
        'fields': [('upper_limit_in_section', 'lower_limit_in_section'),
                   ('error_notes', 'notes')]
    }),

    ('Location Details', {
        'fields': [('longitude', 'latitude'),
                   ('easting', 'northing',),
                   ('geom',)]
    }),
)


class LocalityAdmin(projects.admin.PaleoCoreLocalityAdminGoogle):
    list_display = ('id', 'collection_code', 'locality_number', 'sublocality')
    list_filter = ('collection_code',)
    readonly_fields = ('point_x', 'point_y', 'longitude', 'latitude', 'easting', 'northing')
    search_fields = ('locality_number,', 'id')
    fieldsets = locality_fieldsets
    options = {
        'layers': ['google.terrain']
    }


####################
# Occurrence Admin #
####################
hrp_list_display = ('catalog_number',
                    'barcode',
                    'basis_of_record',
                    'item_type',
                    'collecting_method',
                    'collector',
                    'year_collected',
                    'thumbnail',
                    )

default_list_display = ('barcode', 'field_number', 'catalog_number', 'basis_of_record', 'item_type',
                        'collecting_method', 'collector', 'item_scientific_name', 'item_description',
                        'year_collected',
                        'problem', 'disposition', 'easting', 'northing')

hrp_default_list_select_related = ['recorded_by', 'found_by', 'locality']
hrp_occurrence_list_select_related = hrp_default_list_select_related + ['archaeology', 'biology', 'geology']
hrp_biology_list_select_related = hrp_default_list_select_related + ['taxon']

hrp_list_filter = ['basis_of_record', 'item_type', 'collecting_method', 'collector',
                   'analytical_unit_found', 'drainage_region',
                   'finder', 'year_collected', 'field_number', 'problem', 'disposition',
                   'date_created', 'date_last_modified']

hrp_readonly_fields = ['id', 'catalog_number', 'date_created', 'date_last_modified',
                       'easting', 'northing', 'latitude', 'longitude', 'photo']

hrp_search_fields = ('id',
                     'basis_of_record',
                     'item_type',
                     'barcode',
                     'locality__name', 'locality__collection_code',
                     'locality__locality_number',
                     'item_scientific_name',
                     'item_description',
                     'analytical_unit_found',
                     'analytical_unit_likely',
                     'finder',
                     'collector',
                     'found_by__name',
                     'recorded_by__name',
                     'cat_number',
                     'analytical_unit_found',
                     'analytical_unit_likely',
                     'analytical_unit_simplified'
                     )

hrp_occurrence_fieldsets = (
    ('Record Details', {  # occurrence_details[0]
        'fields': [('id', 'date_created', 'date_last_modified',),
                   ('basis_of_record',),
                   ('remarks',)]
    }),
    ('Occurrence Details', {  # occurrence_fieldsets[1]
        'fields': [('date_recorded', 'year_collected',),
                   ('barcode', 'catalog_number', 'cat_number', 'field_number'),
                   ('item_type', 'item_count'),
                   # ('collector', 'finder', 'collecting_method'), # deprecated fixed choices for people
                   ('recorded_by', 'found_by', 'collecting_method'), # use lookup table choice for people
                   ("locality", "item_number", "item_part"),
                   ('disposition', 'preparation_status'),
                   ('item_description', 'item_scientific_name'),
                   ('collection_remarks',),
                   ('verbatim_kml_data',),
                   ]
    }),
    ('Photos', {  # occurrence_fieldsets[2]
        'fields': [('photo', 'image')],
        # 'classes': ['collapse'],
    }),
    ('Geological Context', {  # occurrence_fieldsets[3]
        'fields': [
            ('analytical_unit_1', 'analytical_unit_2', 'analytical_unit_3'),
            ('analytical_unit_found', 'analytical_unit_likely', 'analytical_unit_simplified'),
            ('in_situ', 'ranked'),
            ('stratigraphic_member',),
            ('drainage_region',)]
    }),
    ('Location Details', {  # occurrence_fieldsets[4]
        'fields': [('collection_code',),
                   ('georeference_remarks',),
                   ('longitude', 'latitude'),
                   ('easting', 'northing',),
                   ('geom',)]
    }),
    ('Problems', {  # lgrp_occurrence_fieldsets[5]
        'fields': [('problem', 'problem_comment'),
                   ],
        'classes': ['collapse']
    }),
)


class OccurrenceResource(resources.ModelResource):
    class Meta:
        model = Occurrence


class OccurrenceAdmin(projects.admin.PaleoCoreOccurrenceAdmin):
    """
    OccurrenceAdmin <- PaleoCoreOccurrenceAdmin <- BingGeoAdmin <- OSMGeoAdmin <- GeoModelAdmin
    """
    resource_class = OccurrenceResource
    list_display = hrp_list_display
    list_select_related = hrp_occurrence_list_select_related
    list_display_links = ['catalog_number', 'barcode', 'basis_of_record']
    list_filter = hrp_list_filter
    readonly_fields = hrp_readonly_fields
    fieldsets = hrp_occurrence_fieldsets
    search_fields = hrp_search_fields
    inlines = [ImagesInline, FilesInline]
    # Use a custom admin changelist page template that includes a button for "Import KMZ"
    # This changelist requires the get_urls() method below to inject the tool_item_url to point to the ImportKMZ view.
    change_list_template = 'admin/projects/projects_change_list.html'
    list_per_page = 500
    options = {
        'layers': ['google.terrain'], 'editable': False, 'default_lat': -122.00, 'default_lon': 38.00,
    }

    def get_urls(self):
        tool_item_urls = [
            path(r'import_kmz/', ImportKMZ.as_view()),
            # path(r'^summary/$',permission_required('mlp.change_occurrence',
            #                         login_url='login/')(self.views.Summary.as_view()),
            #     name="summary"),
        ]
        return tool_item_urls + super(OccurrenceAdmin, self).get_urls()


#################
# Biology Admin #
#################
hrp_biology_list_display = ('catalog_number',
                             'barcode',
                             'basis_of_record',
                             'item_type',
                             'collecting_method',
                             'collector',
                             'taxon',
                             'element',
                             'year_collected',
                             'thumbnail')

biology_inline_fieldsets = (
    ('Taxonomy', {'fields': (('taxon',), 'id')}),
)

hrp_additional_biology_fieldsets = (
    ('Elements', {'fields': [ # hrp_biology_fieldsets[0]
        ('element', 'element_modifier'),
        ('uli1', 'uli2', 'ulc', 'ulp3', 'ulp4', 'ulm1', 'ulm2', 'ulm3'),
        ('uri1', 'uri2', 'urc', 'urp3', 'urp4', 'urm1', 'urm2', 'urm3'),
        ('lri1', 'lri2', 'lrc', 'lrp3', 'lrp4', 'lrm1', 'lrm2', 'lrm3'),
        ('lli1', 'lli2', 'llc', 'llp3', 'llp4', 'llm1', 'llm2', 'llm3'),
        ('indet_incisor', 'indet_canine', 'indet_premolar', 'indet_molar', 'indet_tooth'),
        ('deciduous',),
        ('element_remarks',), ]
    }),
    ('Taxonomy', { # hrp_biology_fieldsets[1]
        'fields': [
            ('taxon', 'identification_qualifier'),
            ('identified_by', 'year_identified', 'type_status'),
            ('taxonomy_remarks',)]
    }),  # biology_additional_fieldsets[1]
    ('Taphonomy', {  # hrp_biology_fieldsets[2]
        'fields': [('weathering', 'surface_modification')],
        # 'classes': ['collapse'],
    }),
)

hrp_biology_fieldsets = (
    hrp_occurrence_fieldsets[0],  # Record Details
    hrp_occurrence_fieldsets[1],  # Details
    hrp_occurrence_fieldsets[2],  # Photos
    hrp_additional_biology_fieldsets[0],  # Elements
    hrp_additional_biology_fieldsets[1],  # Taxonomy
    hrp_additional_biology_fieldsets[2],  # Taphonomy
    hrp_occurrence_fieldsets[3],  # Context
    hrp_occurrence_fieldsets[4],  # Location
    hrp_occurrence_fieldsets[5],  # Problems
)

def get_biology_field_names_for_export():
    """
    Get a list of field names to be included in a full Biology export
    :return:
    """
    b = Biology()
    concrete_fields = b.get_concrete_field_names()
    method_fields = b.method_fields_to_export()
    fk_fields = [f.name for f in b._meta.get_fields() if f.is_relation]
    return concrete_fields + method_fields + fk_fields


class BiologyResource(resources.ModelResource):
    class Meta:
        model = Biology
        fields = Biology().get_concrete_field_names()


class BiologyAdmin(OccurrenceAdmin):
    resource_class = BiologyResource
    list_display = list(hrp_biology_list_display)
    list_select_related = hrp_biology_list_select_related
    fieldsets = hrp_biology_fieldsets
    search_fields = hrp_search_fields + ('taxon__name',)
    actions = ['create_data_csv']

    def create_data_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="HRP_Biology.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer
        o = Occurrence()  # create an empty instance of an occurrence object
        b = Biology()  # create an empty instance of a biology object

        occurrence_field_list = list(o.__dict__.keys())  # fetch the fields names from the instance dictionary
        try:  # try removing the state field from the list
            occurrence_field_list.remove('_state')  # remove the _state field
        except ValueError:  # raised if _state field is not in the dictionary list
            pass
        try:  # try removing the geom field from the list
            occurrence_field_list.remove('geom')
        except ValueError:  # raised if geom field is not in the dictionary list
            pass
        # Replace the geom field with new fields
        occurrence_field_list.append("longitude")  # add new fields for coordinates of the geom object
        occurrence_field_list.append("latitude")
        occurrence_field_list.append("easting")
        occurrence_field_list.append("northing")

        biology_field_list = list(b.__dict__.keys())  # get biology fields
        try:  # try removing the state field
            biology_field_list.remove('_state')
        except ValueError:  # raised if _state field is not in the dictionary list
            pass

        #################################################################
        # For now this method handles all occurrences and corresponding #
        # data from the biology table for faunal occurrences.           #
        #################################################################
        writer.writerow(occurrence_field_list + biology_field_list)  # write column headers

        for occurrence in queryset:  # iterate through the occurrence instances selected in the admin
            # The next line uses string comprehension to build a list of values for each field
            occurrence_dict = occurrence.__dict__
            # Check that instance has geom
            try:
                occurrence_dict['longitude'] = occurrence.longitude()  # translate the occurrence geom object
                occurrence_dict['latitude'] = occurrence.latitude()
                occurrence_dict['easting'] = occurrence.easting()
                occurrence_dict['northing'] = occurrence.northing()
            except AttributeError:  # If no geom data exists write None to the dictionary
                occurrence_dict['longitude'] = None
                occurrence_dict['latitude'] = None
                occurrence_dict['easting'] = None
                occurrence_dict['northing'] = None

            # Next we use the field list to fetch the values from the dictionary.
            # Dictionaries do not have a reliable ordering. This code insures we get the values
            # in the same order as the field list.
            try:  # Try writing values for all keys listed in both the occurrence and biology tables
                writer.writerow([occurrence.__dict__.get(k) for k in occurrence_field_list] +
                                [occurrence.Biology.__dict__.get(k) for k in biology_field_list])
            except ObjectDoesNotExist:  # Django specific exception
                writer.writerow([occurrence.__dict__.get(k) for k in occurrence_field_list])
            except AttributeError:  # Django specific exception
                writer.writerow([occurrence.__dict__.get(k) for k in occurrence_field_list])

        return response
    create_data_csv.short_description = "Download Selected to .csv"


class ArchaeologyAdmin(OccurrenceAdmin):
    list_select_related = hrp_default_list_select_related


class GeologyAdmin(OccurrenceAdmin):
    list_select_related = hrp_default_list_select_related


class PersonResource(resources.ModelResource):

    class Meta:
        model = Person


class PersonAdmin(ImportExportActionModelAdmin):
    resource_class = PersonResource
    list_display = ['id', 'name']
    ordering = ['name']


class TaxonomyResource(resources.ModelResource):
    taxon_path = Field(attribute='full_name', column_name='taxon_path')
    family_name = Field()

    def dehydrate_family_name(self, taxon):
        family = TaxonRank.objects.get(name='Family')

    class Meta:
        model = Taxon
        fields = ['id', 'label', 'taxon_path']


class TaxonAdmin(TaxonomyAdmin):
    # list_display = ['rank', 'name']
    resource_class = TaxonomyResource
    # list_select_related = ['rank', 'parent']


##########################
# Register Admin Classes #
##########################
admin.site.register(Biology, BiologyAdmin)
admin.site.register(Archaeology, ArchaeologyAdmin)
admin.site.register(Geology, GeologyAdmin)
admin.site.register(Hydrology, HydrologyAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(Taxon, TaxonAdmin)
admin.site.register(TaxonRank, TaxonRankAdmin)
admin.site.register(Person, PersonAdmin)
