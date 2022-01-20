from django.contrib.gis import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.urls import reverse, path
from django.utils.html import format_html
#from imagekit.admin import AdminThumbnail

from import_export import resources
import tempfile
import unicodecsv
import os

from .models import *  # import database models from models.py
import projects.admin
from django.forms import TextInput, Textarea  # import custom form widgets
from mapwidgets.widgets import GooglePointFieldWidget
from .views import *
from .utilities import *

#TODO figure out why this is not deleting all the duplicates
def find_and_delete_duplicates(modeladmin, request, queryset):
    dups = find_duplicates(queryset)
    numdel = dups.__len__()

    if 'apply' in request.POST:
        for d in dups:
            d.delete()

        modeladmin.message_user(request,"Deleted {} duplicates".format(numdel))
        return HttpResponseRedirect(request.get_full_path())

    return render(request, 'admin/psr/duplicates.html', context={'items': dups})


CUSTOM_MAP_SETTINGS = {
    "GooglePointFieldWidget": (
        ("mapCenterLocationName", 'Kazakhstan'),
        ("mapCenterLocation", [49.14200071858253, 67.33315509322178]),
    ),
}


psrformfield = {
    models.CharField: {'widget': TextInput(attrs={'size': '50'})},
    models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 75})},
    models.GeometryField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)},
    models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)},
    models.MultiPointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)},
}

default_read_only_fields = ('id', 'geom', 'point_x', 'point_y', 'easting', 'northing', 'date_last_modified', 'date_created', 'last_import', 'date_collected',
                            'basis_of_record', 'collecting_method')

default_occurrence_filter = ['geological_context', 'collector', 'finder',]

lithic_fields = ('dataclass', 'type1', 'type2', 'technique', 'form', 'raw_material', 'raw_material1',
                 'coretype', 'biftype', 'cortex', 'retedge', 'edgedamage', 'alteration', 'scarmorph',
                 'length_mm', 'width_mm', 'thick_mm', 'weight',
                 'platsurf', 'extplat', 'lip', 'pointimpact', 'platwidth', 'platthick', 'epa',
                 'scarlength', 'tqwidth', 'tqthick', 'midwidth', 'midthick', 'tipwidth','tipthick',
                 'lentowid', 'lentothick', 'roew1', 'roet1', 'roew3', 'roet3')

arch_export_fields = ['occurrence_ptr_id', 'archaeology_type',
                      'length_mm', 'width_mm', 'thick_mm', 'weight',
                      'archaeology_remarks', 'archaeology_notes']
bio_export_fields = ['occurrence_ptr_id', 'biology_type',
                     'sex', 'life_stage', 'size_class',
                     'taxon', 'verbatim_taxon', 'identification_qualifier', 'verbatim_identification_qualifier',
                     'taxonomy_remarks', 'type_status', 'fauna_notes']
geo_export_fields = ['occurrence_ptr_id', 'geology_type',
                     'dip', 'strike', 'color', 'texture']
agg_export_fields = ['occurrence_ptr_id', 'counts',
                     'screen_size', 'burning', 'bone', 'microfauna', 'molluscs', 'pebbles',
                     'smallplatforms', 'smalldebris',
                     'tinyplatforms', 'tinydebris',
                     'bull_find_remarks']


#from Django Forum from user kazukiyo923
class ImagesInline(admin.TabularInline):
    model = Image
    extra = 1

    readonly_fields = ("id", "image", "image_preview",)
    fields = ("id", "image_preview", "image", "description", )

    formfield_overrides = { models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 25})} }


class FilesInline(admin.TabularInline):
    model = File
    extra = 0
    readonly_fields = ("id",)


# Define Occurrence resource class for django import-export
class OccurrenceResource(resources.ModelResource):
    class Meta:
        model = Occurrence

#this overrides correctly, but specific forms would need to be made for each admin
# class OccurrenceForm(forms.ModelForm):
#     class Meta:
#         model = Occurrence
#         exclude = ()
#         widgets = {
#             'point': GooglePointFieldWidget,
#             'geom': GooglePointFieldWidget,
#         }


class OccurrenceAdmin(projects.admin.PaleoCoreOccurrenceAdmin):
    resource_class = OccurrenceResource
    #forms = OccurrenceForm
    change_list_template = 'admin/psr/psr_change_list.html'

    # readonly_fields = default_read_only_fields + (
    #     'date_recorded', 'field_number',
    #     'found_by', 'recorded_by', 'collector', 'finder',
    #      'item_type', 'find_type',)

    def get_readonly_fields(self, request, obj=None):
        readonly = []
        fields = default_read_only_fields + (
            'date_recorded', 'field_number',
            'found_by', 'recorded_by', 'collector', 'finder',
            'item_type', 'find_type',)
        if obj is not None:
            for field in fields:
                if obj.__dict__.get(field) not in (None, ''):
                    readonly.append(field)

        return readonly

    list_filter = ['item_type'] + default_occurrence_filter
    search_fields = ['id', 'item_type', 'item_description', 'field_id']
    list_per_page = 500

    list_display = ('field_id', 'item_type', 'find_type', 'geological_context')
    fieldsets = (
        ('Record Details', {
            'fields': [('field_id', 'item_type', 'find_type'),
                       ('item_description'),
                       ('basis_of_record',),
                       ('remarks',),
                       ('date_collected', 'date_created', 'date_last_modified')]
        }),
        ('Find Details', {
            'fields': [('collecting_method',),
                       ('collector', 'recorded_by', 'finder', 'found_by'),
                       ('item_count', 'item_part', 'disposition', 'preparation_status'),
                       ('collection_remarks')
                       ]
        }),
        ('Location', {
            'fields': [ ('geological_context'), ('unit'),
                        ('geom',), ('point')]
        }),
        ('Problems', {
            'fields': [('problem', 'problem_comment'),
                       ],
            'classes': ['collapse']
        }),
    )

    inlines = [ImagesInline]

    save_as = True
    formfield_overrides = psrformfield

    actions = [find_and_delete_duplicates, 'export_simple_csv', 'export_shapefile', 'subtype_arch', 'subtype_bio', 'subtype_geo', 'subtype_agg']

    def export_simple_csv(self, request, queryset):
        fields_to_export = ['id', 'field_id', 'find_type', 'item_description', 'item_type', 'item_count',
                            'finder', 'collector',
                            'basis_of_record', 'collecting_method', 'collection_remarks',
                            'date_collected', 'date_created', 'date_last_modified',
                            'problem', 'problem_comment', 'remarks', 'georeference_remarks',
                            'point', 'geom',]

        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Survey-Occurrences.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(fields_to_export + ['longitude', 'latitude', 'geological_context', 'found_by', 'recorded_by'])  # write column headers
        for o in queryset.order_by('field_id', 'geological_context_id'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                row_list.append(o.point_x())
                row_list.append(o.point_y())
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                if o.recorded_by_id is not None:
                    rb = Person.objects.get(id=o.recorded_by_id)
                    row_list.append(rb.__str__())
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response
    export_simple_csv.short_description = "Export simple report to csv"

    def export_shapefile(self, request, queryset):
        try:
            from StringIO import StringIO
        except ImportError:
            from io import BytesIO as StringIO

        shp = StringIO()
        shx = StringIO()
        dbf = StringIO()
        w = shapefile.Writer(shp=shp, shx=shx, dbf=dbf)

        #TODO figure out the workflow for this to understand what fields need to be exported
        fields_to_export = ['id', 'field_id', 'find_type', 'item_description', 'item_type', 'item_count',
                            'finder', 'collector',
                            'basis_of_record', 'collecting_method', 'collection_remarks',
                            'date_collected', 'date_created', 'date_last_modified',
                            'problem', 'problem_comment', 'remarks', 'georeference_remarks',]

        #create fields
        for f in fields_to_export:
            if f in NUMERICS:
                w.field(f, 'N')
            else:
                w.field(f, 'C')
            w.field("Image", 'C')

        #create records
        for o in queryset.order_by('id'):
            w.point(o.point_x(), o.point_y())
            data = [o.__dict__.get(k) for k in fields_to_export]
            #gc = GeologicalContext.objects.get(id=o.geological_context_id)
            images = Image.objects.get_queryset().filter(occurrence=o)
            ilist = ""
            for i in images:
                name = i.description.split("/")[2]
                ilist = ilist + name + ","
            ilist = ilist[:-1]
            w.record(data[0], data[1], data[2], data[3], data[4],
                     data[5], data[6], data[7], data[8], data[9],
                     data[10], data[11], data[12], data[13], data[14],
                     data[15], data[16], data[17], ilist)

        w.close()

        #zip all all three StringIO objects and write to an HttpResponse
        response = HttpResponse(content_type='application/zip')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Survey-Occurrences.zip"'  # declare the file name
        with ZipFile(response, 'w') as zip_response:
            # Create three files
            with zip_response.open('PSR_Survey-Occurrences.shp', 'w') as file1:
                file1.write(shp.getvalue())
            with zip_response.open('PSR_Survey-Occurrences.shx', 'w') as file2:
                file2.write(shx.getvalue())
            with zip_response.open('PSR_Survey-Occurrences.dbf', 'w') as file3:
                file3.write(dbf.getvalue())
            with zip_response.open('PSR_Survey-Occurrences.prj', 'w') as file4:
                epsg = 'GEOGCS["WGS 84",'
                epsg += 'DATUM["WGS_1984",'
                epsg += 'SPHEROID["WGS 84",6378137,298.257223563]]'
                epsg += ',PRIMEM["Greenwich",0],'
                epsg += 'UNIT["degree",0.0174532925199433]]'
                file4.write(epsg.encode())

        return response
    export_shapefile.short_description = "Export shapefile"

    def subtype_arch(self, request, queryset):
        for q in queryset:
            q.item_type = "Archaeological"
            q.save()
            occurrence2archaeology(q, survey=True)
    subtype_arch.short_description = "Subtype selected as archaeological"

    def subtype_bio(self, request, queryset):
        for q in queryset:
            q.item_type = "Biological"
            q.save()
            occurrence2biology(q, survey=True)
    subtype_bio.short_description = "Subtype selected as biological"

    def subtype_geo(self, request, queryset):
        for q in queryset:
            q.item_type = "Geological"
            q.save()
            occurrence2geo(q, survey=True)
    subtype_geo.short_description = "Subtype selected as geological"

    def subtype_agg(self, request, queryset):
        for q in queryset:
            q.item_type = "Aggregate"
            q.save()
            occurrence2aggr(q, survey=True)
    subtype_agg.short_description = "Subtype selected as aggregate/bulk find"

    def get_urls(self):
        tool_item_urls = [
            path('import_data/', psr.views.ImportShapefileDirectory.as_view())
        ]
        return tool_item_urls + super(OccurrenceAdmin, self).get_urls()


class ExcavationOccurrenceResource(resources.ModelResource):
    class Meta:
        model = ExcavationOccurrence


class ExcavationOccurrenceAdmin(projects.admin.PaleoCoreOccurrenceAdmin):
    resource_class = ExcavationOccurrenceResource
    change_list_template = 'admin/psr/psr_change_list.html'

    readonly_fields = ('id', 'point', 'date_collected', 'field_id',
                       'unit', 'type', 'cat_number', 'date_created',
                       'date_last_modified',
                       'excavator', 'geological_context', 'prism')

    list_display = ('type', 'geological_context', 'cat_number')
    list_filter = ['type', 'geological_context']

    fieldsets = (
        ('Record Details', {
            'fields': [('field_id', 'type',),
                       ('cat_number', 'date_collected',),
                       ('date_created', 'date_last_modified')]
        }),
        ('Find Details', {
            'fields': [('level', 'prism'),
                       ('excavator'),
                       ]
        }),
        ('Location', {
            'fields': [('point'), ('geological_context', 'unit')]
        })
    )

    save_as = True
    formfield_overrides = psrformfield

    actions = [find_and_delete_duplicates, 'export_simple_csv', 'subtype_arch', 'subtype_bio', 'subtype_geo', 'subtype_agg']

    def export_simple_csv(self, request, queryset):
        fields_to_export = ['id', 'field_id', 'cat_number', 'type', 'item_type',
                            'prism', 'point', 'unit', 'level', 'excavator',
                            'date_collected', 'date_created', 'date_last_modified']

        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Excavated-Occurrences.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(fields_to_export + ['longitude', 'latitude', 'geological_context', 'found_by'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                row_list.append(o.point_x())
                row_list.append(o.point_y())
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response
    export_simple_csv.short_description = "Export simple report to csv"

    def subtype_arch(self, request, queryset):
        for q in queryset:
            q.item_type = "Archaeological"
            q.save()
            occurrence2archaeology(q, survey=True)
    subtype_arch.short_description = "Subtype selected as archaeological"

    def subtype_bio(self, request, queryset):
        for q in queryset:
            q.item_type = "Biological"
            q.save()
            occurrence2biology(q, survey=True)
    subtype_bio.short_description = "Subtype selected as biological"

    def subtype_geo(self, request, queryset):
        for q in queryset:
            q.item_type = "Geological"
            q.save()
            occurrence2geo(q, survey=True)
    subtype_geo.short_description = "Subtype selected as geological"

    def subtype_agg(self, request, queryset):
        for q in queryset:
            q.item_type = "Aggregate"
            q.save()
            occurrence2aggr(q, survey=True)
    subtype_agg.short_description = "Subtype selected as aggregate/bulk find"

    def get_urls(self):
        tool_item_urls = [
            path('import_data/', psr.views.ImportAccessDatabase.as_view()),
            # path(r'^summary/$',permission_required('mlp.change_occurrence',
            #                         login_url='login/')(self.views.Summary.as_view()),
            #     name="summary"),
        ]
        return tool_item_urls + super(ExcavationOccurrenceAdmin, self).get_urls()


class GeologicalContextResource(resources.ModelResource):
    class Meta:
        model = GeologicalContext


class GeologicalContextAdmin(projects.admin.PaleoCoreLocalityAdminGoogle):
    resource_class = GeologicalContextResource
    change_list_template = 'admin/psr/psr_geo_change_list.html'

    #readonly_fields = default_read_only_fields + ('date_collected', 'basis_of_record', 'recorded_by')

    def get_readonly_fields(self, request, obj=None):
        readonly = []
        readonly.append('date_last_modified')
        if obj is not None:
            for field in (default_read_only_fields + ('date_collected', 'basis_of_record', 'recorded_by')):
                if obj.__dict__.get(field) not in (None, ''):
                    readonly.append(field)

        return readonly

    list_filter = ['context_type', 'basis_of_record', 'collecting_method', 'geology_type', 'sediment_presence']
    list_per_page = 500
    search_fields = ['id',  'name', 'geology_type', 'context_type']

    list_display = ('name', 'context_type', 'geology_type')
    fieldsets = (
        ('Record Details', {
            'fields': [('name', 'context_type',),
                       ('basis_of_record',),
                       ('notes',),
                       ('date_collected', 'date_created', 'date_last_modified')]
        }),
        ('Find Details', {
            'fields': [('collecting_method',),
                       ('recorded_by',),
                       ]
        }),
        ('Geology Details', {
            'fields': [('geology_type'), ('description'),
                       ('context_remarks')]
        }),
        ('Cave Details', {
            'fields': [('dip', 'strike', 'color', 'texture', 'height', 'width', 'depth'),
                       ('slope_character'), ('sediment_presence', 'sediment_character',),
                       ('cave_mouth_character'), ('rockfall_character'), ('speleothem_character')
                       ],
            'classes': ['collapse']
        }),
        ('Section Details', {
            'fields': [('size_of_loess', 'loess_mean_thickness', 'loess_max_thickness'),
                       ('loess_landscape_position', 'loess_surface_inclination'),
                       ('loess_presence_coarse_components', 'loess_amount_coarse_components'),
                       ('loess_number_sediment_layers', 'loess_number_soil_horizons', 'loess_number_cultural_horizons',
                        'loess_number_coarse_layers'),
                       ],
            'classes': ['collapse']
        }),
        ('Location', {
            'fields': [('geom', 'point')]
        }),
        ('Problems', {
            'fields': [('problem', 'problem_comment'),
                       ('error_notes')
                       ],
            'classes': ['collapse']
        }),
    )

    cave_attributes = ['dip', 'strike', 'color', 'texture', 'height', 'width', 'depth',
                       'slope_character', 'sediment_presence', 'sediment_character',
                       'cave_mouth_character', 'rockfall_character', 'speleothem_character']
    profile_attributes = ['size_of_loess', 'loess_mean_thickness', 'loess_max_thickness',
                          'loess_landscape_position', 'loess_surface_inclination',
                          'loess_presence_coarse_components', 'loess_amount_coarse_components',
                          'loess_number_sediment_layers', 'loess_number_soil_horizons',
                          'loess_number_cultural_horizons', 'loess_number_coarse_layers',
                          'loess_presence_vertical_profile']

    save_as = True
    formfield_overrides = psrformfield

    inlines = [ImagesInline]

    actions = [find_and_delete_duplicates, 'export_simple_csv', 'export_shapefile', 'export_photos']

    def export_simple_csv(self, request, queryset):
        fields_to_export = ['id', 'name', 'context_type', 'geology_type', 'description',
                            'dip', 'strike', 'color', 'texture', 'height', 'width', 'depth',
                            'slope_character', 'sediment_presence', 'sediment_character',
                            'cave_mouth_character', 'rockfall_character', 'speleothem_character',
                            'size_of_loess', 'loess_mean_thickness', 'loess_max_thickness',
                            'loess_landscape_position', 'loess_surface_inclination',
                            'loess_presence_coarse_components', 'loess_amount_coarse_components',
                            'loess_number_sediment_layers', 'loess_number_soil_horizons',
                            'loess_number_cultural_horizons', 'loess_number_coarse_layers',
                            'loess_presence_vertical_profile',
                            'point', 'geom','basis_of_record', 'collecting_method',
                            'date_collected', 'date_created', 'date_last_modified',
                            'problem', 'problem_comment', 'remarks', 'georeference_remarks']

        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Geological-Contexts.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(fields_to_export + ['longitude', 'latitude', 'found_by'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                row_list.append(o.point_x())
                row_list.append(o.point_y())
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response
    export_simple_csv.short_description = "Export simple report to csv"

    def export_shapefile(self, request, queryset):
        try:
            from StringIO import StringIO
        except ImportError:
            from io import BytesIO as StringIO

        shp = StringIO()
        shx = StringIO()
        dbf = StringIO()
        w = shapefile.Writer(shp=shp, shx=shx, dbf=dbf)

        #TODO figure out the workflow for this to understand what fields need to be exported
        fields_to_export = ['id', 'name', 'context_type', 'geology_type', 'description',
                            'dip', 'strike', 'color', 'texture', 'height', 'width', 'depth',
                            'slope_character', 'sediment_presence', 'sediment_character',
                            'cave_mouth_character', 'rockfall_character', 'speleothem_character',
                            'size_of_loess', 'loess_mean_thickness', 'loess_max_thickness',
                            'loess_landscape_position', 'loess_surface_inclination',
                            'loess_presence_coarse_components', 'loess_amount_coarse_components',
                            'loess_number_sediment_layers', 'loess_number_soil_horizons',
                            'loess_number_cultural_horizons', 'loess_number_coarse_layers',
                            'loess_presence_vertical_profile',
                            'point', 'geom', 'basis_of_record', 'collecting_method',
                            'date_collected', 'date_created', 'date_last_modified',
                            'problem', 'problem_comment', 'remarks', 'georeference_remarks']

        #create fields
        for f in fields_to_export:
            if f in NUMERICS:
                w.field(f, 'N')
            else:
                w.field(f, 'C')
        w.field("Image", 'C')

        #create records
        for o in queryset.order_by('id'):
            #print(o.name)
            w.point(o.point_x(), o.point_y())
            data = [o.__dict__.get(k) for k in fields_to_export]
            images = Image.objects.get_queryset().filter(locality=o,occurrence__isnull=True)
            ilist = ""
            for i in images:
                name = i.description.split("/")[2]
                ilist = ilist + name + ","
            ilist = ilist[:-1]

            w.record(data[0], data[1], data[2], data[3], data[4],
                     data[5], data[6], data[7], data[8], data[9],
                     data[10], data[11], data[12], data[13], data[14],
                     data[15], data[16], data[17], data[18], data[19],
                     data[20], data[21], data[22], data[23], data[24],
                     data[25], data[26], data[27], data[28], data[29],
                     data[30], data[31], data[32], data[33], data[34],
                     data[35], data[36], data[37], data[38], data[39],
                     data[40], ilist)

        w.close()

        #zip all all three StringIO objects and write to an HttpResponse
        response = HttpResponse(content_type='application/zip')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Geological-Contexts.zip"'  # declare the file name
        with ZipFile(response, 'w') as zip_response:
            with zip_response.open('PSR_Geological-Contexts.shp', 'w') as file1:
                file1.write(shp.getvalue())
            with zip_response.open('PSR_Geological-Contexts.shx', 'w') as file2:
                file2.write(shx.getvalue())
            with zip_response.open('PSR_Geological-Contexts.dbf', 'w') as file3:
                file3.write(dbf.getvalue())
            with zip_response.open('PSR_Geological-Contexts.prj', 'w') as file4:
                epsg = 'GEOGCS["WGS 84",'
                epsg += 'DATUM["WGS_1984",'
                epsg += 'SPHEROID["WGS 84",6378137,298.257223563]]'
                epsg += ',PRIMEM["Greenwich",0],'
                epsg += 'UNIT["degree",0.0174532925199433]]'
                file4.write(epsg.encode())

        return response
    export_shapefile.short_description = "Export shapefile"

    def export_photos(self, request, queryset):
        response = HttpResponse(content_type='application/zip')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="Geological-Context_Photos.zip"'

        with ZipFile(response, 'w') as zip_response:
            for o in queryset:
                images = Image.objects.get_queryset().filter(locality=o)
                dirname = o.name
                print(dirname)

                for i in images:
                    name = i.description.split("/")[2]
                    filename = os.path.join("media/uploads/images/", i.description)
                    print(filename)
                    directory = dirname + "/" + os.path.basename(filename)
                    zip_response.write(filename=filename, arcname=directory)

        return response
    export_photos.short_description = "Export photos"

    def get_urls(self):
        tool_item_urls = [
            path('import_data/', psr.views.ImportShapefileDirectory.as_view()),
            # path(r'^summary/$',permission_required('mlp.change_occurrence',
            #                         login_url='login/')(self.views.Summary.as_view()),
            #     name="summary"),
            path('import_json/', psr.views.ImportJSON.as_view()),
        ]
        return tool_item_urls + super(GeologicalContextAdmin, self).get_urls()


class LithicInline(admin.StackedInline):
    model = Lithic
    extra = 0
    fk_name = 'archaeology_ptr'
    readonly_fields = ['archaeology_ptr_id']
    fields = lithic_fields


class CeramicInline(admin.StackedInline):
    model = Ceramic
    extra = 0
    fk_name = 'archaeology_ptr'
    readonly_fields = ['archaeology_ptr_id']
    fields = ('type', 'decorated')


class BoneInline(admin.StackedInline):
    model = Bone
    extra = 0
    fk_name = 'archaeology_ptr'
    readonly_fields = ['archaeology_ptr_id']
    fields = ('part', 'cutmarks', 'burning')


class ArchaeologyResource(resources.ModelResource):
    class Meta:
        model = Archaeology


class ArchaeologyAdmin(OccurrenceAdmin):
    change_list_template = 'admin/change_list.html'

    model = Archaeology
    resource_class = ArchaeologyResource
    # empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'archaeology_type', 'geological_context')
    list_filter = ['archaeology_type'] + default_occurrence_filter

    formfield_overrides = psrformfield
    fieldsets = (OccurrenceAdmin.fieldsets[0],
                 OccurrenceAdmin.fieldsets[1],
                 ('Archaeology Details', {
                     'fields': [('archaeology_type', 'period'),
                                ('length_mm', 'width_mm', 'thick_mm', 'weight', ),
                                ('archaeology_remarks', ),
                                ]
                 }),
                 OccurrenceAdmin.fieldsets[2])

    actions = [find_and_delete_duplicates, 'export_simple_csv', 'subtype_lithic', 'subtype_bone', 'subtype_ceramic']

    inlines = [LithicInline, BoneInline, CeramicInline, ImagesInline]

    def export_simple_csv(self, request, queryset):
        fields_to_export = arch_export_fields
        occurrence_export = ['field_id', 'find_type', 'item_description', 'item_type', 'item_count',
                             'finder', 'collector', 'collecting_method', 'date_collected',
                             'point', 'geom']
        lithic_export = list(lithic_fields)
        ceramic_export = ['type', 'decorated']
        bone_export = ['cutmarks', 'burning', 'part']

        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Survey-Archaeology.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(fields_to_export + ['longitude', 'latitude', 'found_by'] + occurrence_export + lithic_export + ceramic_export + bone_export +
                        ['geological_context'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                row_list.append(o.point_x())
                row_list.append(o.point_y())
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                row_list = row_list + [o.__dict__.get(k) for k in occurrence_export]
                if o.__dict__.get('find_type') in PSR_LITHIC_VOCABULARY:
                    l = Lithic.objects.get(id=o.__dict__.get('id'))
                    row_list = row_list + [l.__dict__.get(k) for k in lithic_export]
                else:
                    row_list = row_list + [None for k in lithic_export]
                if o.__dict__.get('find_type') in PSR_CERAMIC_VOCABULARY:
                    c = Ceramic.objects.get(id=o.__dict__.get('id'))
                    row_list = row_list + [c.__dict__.get(k) for k in ceramic_export]
                else:
                    row_list = row_list + [None for k in ceramic_export]
                if o.__dict__.get('find_type') in PSR_BONE_VOCABULARY:
                    b = Ceramic.objects.get(id=o.__dict__.get('id'))
                    row_list = row_list + [b.__dict__.get(k) for k in ceramic_export]
                else:
                    row_list = row_list + [None for k in bone_export]
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response
    export_simple_csv.short_description = "Export simple report to csv"

    def subtype_lithic(self, request, queryset):
        for q in queryset:
            archaeology2lithic(q, survey=True)
    subtype_lithic.short_description = "Subtype selected as survey lithic(s)"

    def subtype_bone(self, request, queryset):
        for q in queryset:
            archaeology2bone(q, survey=True)
    subtype_bone.short_description = "Subtype selected as survey bone(s)"

    def subtype_ceramic(self, request, queryset):
        for q in queryset:
            archaeology2ceramic(q, survey=True)
    subtype_ceramic.short_description = "Subtype selected as survey ceramic(s)"


class BiologyResource(resources.ModelResource):
    class Meta:
        model = Biology


class BiologyAdmin(OccurrenceAdmin):
    change_list_template = 'admin/change_list.html'

    model = Biology
    resource_class = BiologyResource
    # empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'biology_type', 'geological_context')
    list_filter = ['biology_type'] + default_occurrence_filter

    formfield_overrides = psrformfield
    fieldsets = (OccurrenceAdmin.fieldsets[0],
                 OccurrenceAdmin.fieldsets[1],
                 ('Biology Details', {
                     'fields': [('biology_type', ),
                                ('sex', 'life_stage', 'size_class',),
                                ('verbatim_taxon', 'identification_qualifier'),
                                ]
                 }),
                 OccurrenceAdmin.fieldsets[2])

    fields_to_export = bio_export_fields

    actions = [find_and_delete_duplicates, 'export_simple_csv']

    def export_simple_csv(self, request, queryset):
        fields_to_export = bio_export_fields
        occurrence_export = ['field_id', 'find_type', 'item_description', 'item_type', 'item_count',
                             'finder', 'collector', 'collecting_method', 'date_collected',
                             'point', 'geom']
        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Survey-Bio.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(
            fields_to_export + ['found_by'] + occurrence_export + ['geological_context'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                row_list = row_list + [o.__dict__.get(k) for k in occurrence_export]
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response

    export_simple_csv.short_description = "Export simple report to csv"


class GeologyResource(resources.ModelResource):
    class Meta:
        model = Geology


class GeologyAdmin(OccurrenceAdmin):
    change_list_template = 'admin/change_list.html'

    model = Geology
    resource_class = GeologyResource
    # empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'geology_type', 'geological_context')
    list_filter = ['geology_type'] + default_occurrence_filter

    formfield_overrides = psrformfield
    fieldsets = (OccurrenceAdmin.fieldsets[0],
                 OccurrenceAdmin.fieldsets[1],
                 ('Geology Details', {
                     'fields': [('geology_type',),
                                ('dip', 'strike', 'color', 'texture'),
                                ]
                 }),
                 OccurrenceAdmin.fieldsets[2])

    fields_to_export = geo_export_fields

    actions = [find_and_delete_duplicates, 'export_simple_csv']

    def export_simple_csv(self, request, queryset):
        fields_to_export = geo_export_fields
        occurrence_export = ['field_id', 'find_type', 'item_description', 'item_type', 'item_count',
                             'finder', 'collector', 'collecting_method', 'date_collected',
                             'point', 'geom']
        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Survey-Geo.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(
            fields_to_export + ['found_by'] + occurrence_export + ['geological_context'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                row_list = row_list + [o.__dict__.get(k) for k in occurrence_export]
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response

    export_simple_csv.short_description = "Export simple report to csv"


class AggregateResource(resources.ModelResource):
    class Meta:
        model = Aggregate


class AggregateAdmin(OccurrenceAdmin):
    change_list_template = 'admin/change_list.html'

    model = Aggregate
    resource_class = AggregateResource
    # empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'screen_size', 'geological_context')
    list_filter = default_occurrence_filter

    formfield_overrides = psrformfield
    fieldsets = (OccurrenceAdmin.fieldsets[0],
                 OccurrenceAdmin.fieldsets[1],
                 ('Aggregate Details', {
                     'fields': [('screen_size', 'counts'),
                                ('burning', 'bone', 'microfauna', 'molluscs', 'pebbles'),
                                ('smallplatforms', 'smalldebris', 'tinyplatforms', 'tinydebris'),
                                ('bull_find_remarks')
                                ]
                 }),
                 OccurrenceAdmin.fieldsets[2])

    fields_to_export = agg_export_fields

    actions = [find_and_delete_duplicates, 'export_simple_csv']

    def export_simple_csv(self, request, queryset):
        fields_to_export = agg_export_fields
        occurrence_export = ['field_id', 'find_type', 'item_description', 'item_type', 'item_count',
                             'finder', 'collector', 'collecting_method', 'date_collected',
                             'point', 'geom']
        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Survey-Aggregates.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(
            fields_to_export + ['found_by'] + occurrence_export + ['geological_context'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                row_list = row_list + [o.__dict__.get(k) for k in occurrence_export]
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response

    export_simple_csv.short_description = "Export simple report to csv"


class ExcavLithicInline(admin.StackedInline):
    model = ExcavatedLithic
    extra = 0
    fk_name = 'excavatedarchaeology_ptr'
    readonly_fields = ['excavatedarchaeology_ptr_id']
    fields = lithic_fields


class ExcavCeramicInline(admin.StackedInline):
    model = ExcavatedCeramic
    extra = 0
    fk_name = 'excavatedarchaeology_ptr'
    readonly_fields = ['excavatedarchaeology_ptr_id']
    fields = ('type', 'decorated')


class ExcavBoneInline(admin.StackedInline):
    model = ExcavatedBone
    extra = 0
    fk_name = 'excavatedarchaeology_ptr'
    readonly_fields = ['excavatedarchaeology_ptr_id']
    fields = ('part', 'cutmarks', 'burning')


class ExcavatedArchaeologyResource(resources.ModelResource):
    class Meta:
        model = ExcavatedArchaeology


class ExcavatedArchaeologyAdmin(ExcavationOccurrenceAdmin):
    change_list_template = 'admin/change_list.html'

    model = ExcavatedArchaeology
    resource_class = ExcavatedArchaeologyResource
    # empty_value_display = '-empty-'
    list_display = ('excavationoccurrence_ptr_id', 'archaeology_type', 'geological_context')

    formfield_overrides = psrformfield
    fieldsets = (ExcavationOccurrenceAdmin.fieldsets[0],
                 ('Find Details', {
                     'fields': [('archaeology_type', 'period'),
                                ('length_mm', 'width_mm', 'thick_mm', 'weight', ),
                                ('archaeology_remarks', ),
                                ('level', 'prism'),
                                ('excavator'),
                                ]
                 }),
                 ExcavationOccurrenceAdmin.fieldsets[2])

    fields_to_export = arch_export_fields

    inlines = [ExcavLithicInline, ExcavBoneInline, ExcavCeramicInline]

    actions = [find_and_delete_duplicates, 'export_simple_csv', 'subtype_lithic', 'subtype_bone', 'subtype_ceramic']

    def export_simple_csv(self, request, queryset):
        fields_to_export = arch_export_fields
        occurrence_export = ['id', 'field_id', 'cat_number', 'type', 'item_type',
                             'prism', 'point', 'unit', 'level', 'excavator']
        lithic_export = list(lithic_fields)
        ceramic_export = ['type', 'decorated']
        bone_export = ['cutmarks', 'burning', 'part']

        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Excavated-Archaeology.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(fields_to_export + ['found_by'] + occurrence_export + lithic_export + ceramic_export + bone_export+ ['geological_context'])   # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                row_list = row_list + [o.__dict__.get(k) for k in occurrence_export]
                if o.__dict__.get('find_type') in PSR_LITHIC_VOCABULARY:
                    l = Lithic.objects.get(id=o.__dict__.get('id'))
                    row_list = row_list + [l.__dict__.get(k) for k in lithic_export]
                else:
                    row_list = row_list + [None for k in lithic_export]
                if o.__dict__.get('find_type') in PSR_CERAMIC_VOCABULARY:
                    c = Ceramic.objects.get(id=o.__dict__.get('id'))
                    row_list = row_list + [c.__dict__.get(k) for k in ceramic_export]
                else:
                    row_list = row_list + [None for k in ceramic_export]
                if o.__dict__.get('find_type') in PSR_BONE_VOCABULARY:
                    b = Ceramic.objects.get(id=o.__dict__.get('id'))
                    row_list = row_list + [b.__dict__.get(k) for k in ceramic_export]
                else:
                    row_list = row_list + [None for k in bone_export]
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response
    export_simple_csv.short_description = "Export simple report to csv"

    def subtype_lithic(self, request, queryset):
        for q in queryset:
            archaeology2lithic(q, survey=False)
    subtype_lithic.short_description = "Subtype selected as excavated lithic(s)"

    def subtype_bone(self, request, queryset):
        for q in queryset:
            archaeology2bone(q, survey=False)
    subtype_bone.short_description = "Subtype selected as excavated bone(s)"

    def subtype_ceramic(self, request, queryset):
        for q in queryset:
            archaeology2ceramic(q, survey=False)
    subtype_ceramic.short_description = "Subtype selected as excavated ceramic(s)"


class ExcavatedBiologyResource(resources.ModelResource):
    class Meta:
        model = ExcavatedBiology


class ExcavatedBiologyAdmin(ExcavationOccurrenceAdmin):
    change_list_template = 'admin/change_list.html'

    model = ExcavatedBiology
    resource_class = BiologyResource
    # empty_value_display = '-empty-'
    list_display = ('excavationoccurrence_ptr_id', 'biology_type', 'geological_context')

    formfield_overrides = psrformfield
    fieldsets = (ExcavationOccurrenceAdmin.fieldsets[0],
                 ('Find Details', {
                     'fields': [('biology_type', ),
                                ('sex', 'life_stage', 'size_class', ),
                                ('taxon', 'identification_qualifier'),
                                ('level', 'prism'),
                                ('excavator'),
                                ]
                 }),
                 ExcavationOccurrenceAdmin.fieldsets[2])

    actions = [find_and_delete_duplicates, 'export_simple_csv']

    def export_simple_csv(self, request, queryset):
        fields_to_export = bio_export_fields
        occurrence_export = ['id', 'field_id', 'cat_number', 'type', 'item_type',
                             'prism', 'point', 'unit', 'level', 'excavator']

        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Excavated-Bio.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(fields_to_export + ['found_by'] + occurrence_export + ['geological_context'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                row_list = row_list + [o.__dict__.get(k) for k in occurrence_export]
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response
    export_simple_csv.short_description = "Export simple report to csv"


class ExcavatedGeologyResource(resources.ModelResource):
    class Meta:
        model = ExcavatedGeology


class ExcavatedGeologyAdmin(ExcavationOccurrenceAdmin):
    change_list_template = 'admin/change_list.html'

    model = ExcavatedGeology
    resource_class = ExcavatedGeologyResource
    # empty_value_display = '-empty-'
    list_display = ('excavationoccurrence_ptr_id', 'geology_type', 'geological_context')

    formfield_overrides = psrformfield
    fieldsets = (ExcavationOccurrenceAdmin.fieldsets[0],
                 ('Find Details', {
                     'fields': [('geology_type'),
                                ('color', 'texture'),
                                ('level', 'prism'),
                                ('excavator'),
                                ]
                 }),
                 ExcavationOccurrenceAdmin.fieldsets[2])

    actions = [find_and_delete_duplicates, 'export_simple_csv']

    def export_simple_csv(self, request, queryset):
        fields_to_export = geo_export_fields
        occurrence_export = ['id', 'field_id', 'cat_number', 'type', 'item_type',
                             'prism', 'point', 'unit', 'level', 'excavator']

        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Excavated-Geo.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(fields_to_export + ['found_by'] + occurrence_export + ['geological_context'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                row_list = row_list + [o.__dict__.get(k) for k in occurrence_export]
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response
    export_simple_csv.short_description = "Export simple report to csv"


class ExcavatedAggregateResource(resources.ModelResource):
    class Meta:
        model = ExcavatedAggregate


class ExcavatedAggregateAdmin(ExcavationOccurrenceAdmin):
    change_list_template = 'admin/change_list.html'

    model = ExcavatedAggregate
    resource_class = ExcavatedAggregateResource
    # empty_value_display = '-empty-'
    list_display = ('excavationoccurrence_ptr_id', 'screen_size', 'geological_context')

    formfield_overrides = psrformfield
    fieldsets = (ExcavationOccurrenceAdmin.fieldsets[0],
                 ('Find Details', {
                     'fields': [('screen_size', 'counts'),
                                ('burning', 'bone', 'microfauna', 'molluscs', 'pebbles'),
                                ('smallplatforms', 'smalldebris', 'tinyplatforms', 'tinydebris'),
                                ('level', 'prism'),
                                ('excavator'),
                                ]
                 }),
                 ExcavationOccurrenceAdmin.fieldsets[2])

    actions = [find_and_delete_duplicates, 'export_simple_csv']

    def export_simple_csv(self, request, queryset):
        fields_to_export = agg_export_fields
        occurrence_export = ['id', 'field_id', 'cat_number', 'type', 'item_type',
                             'prism', 'point', 'unit', 'level', 'excavator']

        response = HttpResponse(content_type='text/csv')  # declare the response type
        response['Content-Disposition'] = 'attachment; filename="PSR_Excavated-Buckets.csv"'  # declare the file name
        writer = unicodecsv.writer(response)  # open a .csv writer

        writer.writerow(fields_to_export + ['found_by'] + occurrence_export + ['geological_context'])  # write column headers
        for o in queryset.order_by('field_id', 'barcode'):
            try:
                row_list = [o.__dict__.get(k) for k in fields_to_export]
                if o.found_by_id is not None:
                    fb = Person.objects.get(id=o.found_by_id)
                    row_list.append(fb.__str__())
                row_list = row_list + [o.__dict__.get(k) for k in occurrence_export]
                gc = GeologicalContext.objects.get(id=o.geological_context_id)
                row_list.append(gc.name)
                writer.writerow(row_list)
            except:
                writer.writerow(o.id)
        return response
    export_simple_csv.short_description = "Export simple report to csv"


admin.site.register(Biology, BiologyAdmin)
admin.site.register(Archaeology, ArchaeologyAdmin)
admin.site.register(Geology, GeologyAdmin)
admin.site.register(GeologicalContext, GeologicalContextAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(ExcavationOccurrence, ExcavationOccurrenceAdmin)
admin.site.register(ExcavatedBiology, ExcavatedBiologyAdmin)
admin.site.register(ExcavatedArchaeology, ExcavatedArchaeologyAdmin)
admin.site.register(ExcavatedGeology, ExcavatedGeologyAdmin)
admin.site.register(Aggregate, AggregateAdmin)
admin.site.register(ExcavatedAggregate, ExcavatedAggregateAdmin)
