# Django imports
from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.forms import TextInput, Textarea  # import custom form widgets

# Third party imports
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mapwidgets.widgets import GooglePointFieldWidget

# App imports
from sermar.models import Locality, Collection, Biology


# Admin Classes
class LocalityAdmin(admin.ModelAdmin):
    list_display = ['roost_id', 'landmark', 'priority', 'in_park', 'pellets', 'bones', 'analysis',
                    'owl_species', 'pellet_species', 'verbatim_roost_type', 'accumulating_agent', 'protected_area']
    list_filter = ['pellets', 'bones', 'analysis', 'accumulating_agent', 'protected_area']
    readonly_fields = ['easting', 'northing', 'longitude', 'latitude']

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
    list_display = ['collection_code', 'locality', 'date', 'disposition', 'specimen_loc', 'sample_size',
                    'source', 'status', 'bags']
    list_filter = ['source', 'specimen_loc', 'locality']
    search_fields = ['collection_code', 'locality__name', 'locality__roost_id']

    resource_class = CollectionResource


class BiologyResource(resources.ModelResource):

    class Meta:
        model = Biology


class BiologyAdmin(ImportExportModelAdmin):
    list_display = ['id', 'collection', 'morphotype_id', 'element_id',  'loan', 'disposition']
    list_filter = ['collection_code', 'loan', 'morphotype_id']
    search_fields = ['id']

    resource_class = BiologyResource


# Admin Registration
admin.site.register(Biology, BiologyAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Collection, CollectionAdmin)
