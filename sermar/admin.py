from django.contrib.gis import admin
from mapwidgets.widgets import GooglePointFieldWidget
from sermar.models import Locality, Collection, Biology
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class LocalityAdmin(admin.ModelAdmin):
    list_display = ['roost_id', 'landmark', 'priority', 'in_park', 'pellets', 'bones', 'analysis',
                    'owl_species', 'pellet_species', 'verbatim_roost_type']


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


admin.site.register(Biology, BiologyAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Collection, CollectionAdmin)
