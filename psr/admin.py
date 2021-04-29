from django.contrib.gis import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.urls import reverse, path
from django.utils.html import format_html
#from imagekit.admin import AdminThumbnail

from import_export import resources
import unicodecsv

from .models import *  # import database models from models.py
import projects.admin
from django.forms import TextInput, Textarea  # import custom form widgets
from mapwidgets.widgets import GooglePointFieldWidget
from .views import *
from .utilities import *

psr_gc_fieldsets = (
    ('Record Details', {
        'fields': [('name', 'context_type',),
                   ('basis_of_record', 'collecting_method'),
                   ('recorded_by'),
                   ('remarks',),
                   ('date_collected', 'date_created', 'date_last_modified')]
    }),
    ('Geology Details', {
        'fields': [('geology_type'), ('description'),
                   ]
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

psrformfield = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 75})},
        models.PointField: {"widget": GooglePointFieldWidget}
    }

default_read_only_fields = ('id', 'geom', 'point_x', 'point_y', 'easting', 'northing', 'date_last_modified',
                            'name', 'date_created', 'last_import', 'collecting_method',)

default_occurrence_filter = ['geological_context', 'collector', 'finder',]

lithic_fields = ('dataclass', 'type1', 'type2', 'technique', 'form', 'raw_material', 'raw_material1',
              'coretype', 'biftype', 'cortex', 'retedge', 'edgedamage', 'alteration', 'scarmorph',
              'length_mm', 'width_mm', 'thick_mm', 'weight',
              'platsurf', 'extplat', 'lip', 'pointimpact', 'platwidth', 'platthick', 'epa',
              'scarlength', 'tqwidth', 'tqthick', 'midwidth', 'midthick', 'tipwidth','tipthick',
              'lentowid', 'lentothick', 'roew1', 'roet1', 'roew3', 'roet3')


#from stackoverflow
#TODO fix thumbnails
class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and getattr(value, 'url', None):
            html = format_html('<a href="{0}" target="_blank"><img src="{0}" alt="{1}" width="150" height="150" style="object-fit: contain;"/></a>', value.url, str(value)) + html
        return html


class ImagesInline(admin.TabularInline):
    model = Image
    extra = 1
    #image_display = AdminThumbnail(image_field='image')

    readonly_fields = ("id", "image")
    fields = ("id", "image_display", "description")
    # formfield_overrides = {
    #     models.ImageField: {'widget': AdminImageWidget}
    # }




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
    change_list_template = 'admin/psr/psr_change_list.html'

    readonly_fields = default_read_only_fields + (
    'date_recorded', 'field_number', 'basis_of_record', 'found_by', 'collector', 'finder') + \
                      ('field_id', 'item_type', 'find_type', 'name')
    list_filter = ['item_type'] + default_occurrence_filter
    search_fields = ['id', 'item_type', 'item_description', 'barcode', 'field_id']
    list_per_page = 500

    list_display = ('field_id', 'item_type', 'find_type', 'geological_context')
    fieldsets = (
    ('Record Details', {
        'fields': [('field_id', 'item_type', 'find_type', 'name'),
                   ('item_description'),
                   ('basis_of_record',),
                   ('remarks',),
                   ('date_recorded', 'date_created', 'date_last_modified')]
    }),  # lgrp_occurrence_fieldsets[0]
    ('Find Details', {
        'fields': [('collecting_method',),
                   ('collector', 'finder', 'found_by'),
                   ('item_count', 'field_number',),
                   ]
    }),
    ('Location', {
        'fields': [('geom',), ('point')]
    }),  # lgrp_occurrence_fieldsets[4]
    ('Problems', {
        'fields': [('problem', 'problem_comment'),
                   ],
        'classes': ['collapse']
    }),  # lgrp_occurrence_fieldsets[5]
)

    inlines = [ImagesInline]

    save_as = True
    formfield_overrides = psrformfield

    actions = ['subtype_arch', 'subtype_bio', 'subtype_geo', 'subtype_agg']

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
            path(r'import_data/', psr.views.ImportShapefile.as_view()),
            # path(r'^summary/$',permission_required('mlp.change_occurrence',
            #                         login_url='login/')(self.views.Summary.as_view()),
            #     name="summary"),
        ]
        return tool_item_urls + super(OccurrenceAdmin, self).get_urls()


class ExcavationOccurrenceResource(resources.ModelResource):
    class Meta:
        model = ExcavationOccurrence


class ExcavationOccurrenceAdmin(projects.admin.PaleoCoreOccurrenceAdmin):
    resource_class = ExcavationOccurrenceResource
    change_list_template = 'admin/psr/psr_change_list.html'

    readonly_fields = ('id', 'point', 'date_collected', 'field_id', 'unit', 'type', 'cat_number', 'date_created',
                       'date_last_modified') + \
                      ('excavator', 'geological_context')

    list_display = ('type', 'geological_context', 'cat_number')
    list_filter = ['type', 'geological_context']

    fieldsets = (
        ('Record Details', {
            'fields': [('field_id', 'type',),
                       ('cat_number', 'date_collected',),
                       ('date_created', 'date_last_modified')]
        }),  # lgrp_occurrence_fieldsets[0]
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

    actions = ['subtype_arch', 'subtype_bio', 'subtype_geo', 'subtype_agg']

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
            path(r'import_data/', psr.views.ImportAccessDatabase.as_view()),
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
    change_list_template = 'admin/psr/psr_change_list.html'

    readonly_fields = default_read_only_fields + ('date_collected', 'context_type', 'basis_of_record', 'recorded_by')
    list_filter = ['context_type', 'basis_of_record', 'collecting_method', 'geology_type', 'sediment_presence']
    list_per_page = 500
    search_fields = ['id', 'item_scientific_name', 'item_description', 'barcode', 'cat_number', 'name', 'geology_type',
                     'context_type']

    list_display = ('name', 'context_type', 'geology_type')
    fieldsets = psr_gc_fieldsets

    save_as = True
    formfield_overrides = psrformfield

    inlines = [ImagesInline]

    def get_urls(self):
        tool_item_urls = [
            path(r'import_data/', psr.views.ImportShapefile.as_view()),
            # path(r'^summary/$',permission_required('mlp.change_occurrence',
            #                         login_url='login/')(self.views.Summary.as_view()),
            #     name="summary"),
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
    model = Archaeology
    resource_class = ArchaeologyResource
    # empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'archaeology_type', 'geological_context')
    list_filter = ['archaeology_type'] + default_occurrence_filter

    formfield_overrides = psrformfield

    actions = ['subtype_lithic', 'subtype_bone', 'subtype_ceramic']

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

    inlines = [LithicInline, BoneInline, CeramicInline, ImagesInline]

    #TODO figure out how to do conditional inline statement


class BiologyResource(resources.ModelResource):
    class Meta:
        model = Biology


class BiologyAdmin(OccurrenceAdmin):
    model = Biology
    resource_class = BiologyResource
    # empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'biology_type', 'geological_context')
    list_filter = ['biology_type'] + default_occurrence_filter

    formfield_overrides = psrformfield


class GeologyResource(resources.ModelResource):
    class Meta:
        model = Geology


class GeologyAdmin(OccurrenceAdmin):
    model = Geology
    resource_class = GeologyResource
    # empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'geology_type', 'geological_context')
    list_filter = ['geology_type'] + default_occurrence_filter

    formfield_overrides = psrformfield


class AggregateResource(resources.ModelResource):
    class Meta:
        model = Aggregate


class AggregateAdmin(OccurrenceAdmin):
    model = Aggregate
    resource_class = AggregateResource
    # empty_value_display = '-empty-'
    list_display = ('occurrence_ptr_id', 'screen_size', 'geological_context')
    list_filter = default_occurrence_filter

    formfield_overrides = psrformfield


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
    model = ExcavatedArchaeology
    resource_class = ExcavatedArchaeologyResource
    # empty_value_display = '-empty-'
    list_display = ('excavationoccurrence_ptr_id', 'archaeology_type', 'geological_context')

    formfield_overrides = psrformfield

    inlines = [ExcavLithicInline, ExcavBoneInline, ExcavCeramicInline]

    actions = ['subtype_lithic', 'subtype_bone', 'subtype_ceramic']

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
    model = ExcavatedBiology
    resource_class = BiologyResource
    # empty_value_display = '-empty-'
    list_display = ('excavationoccurrence_ptr_id', 'biology_type', 'geological_context')

    formfield_overrides = psrformfield


class ExcavatedGeologyResource(resources.ModelResource):
    class Meta:
        model = ExcavatedGeology


class ExcavatedGeologyAdmin(ExcavationOccurrenceAdmin):
    model = ExcavatedGeology
    resource_class = ExcavatedGeologyResource
    # empty_value_display = '-empty-'
    list_display = ('excavationoccurrence_ptr_id', 'geology_type', 'geological_context')

    formfield_overrides = psrformfield


class ExcavatedAggregateResource(resources.ModelResource):
    class Meta:
        model = ExcavatedAggregate


class ExcavatedAggregateAdmin(ExcavationOccurrenceAdmin):
    model = ExcavatedAggregate
    resource_class = ExcavatedAggregateResource
    # empty_value_display = '-empty-'
    list_display = ('excavationoccurrence_ptr_id', 'screen_size', 'geological_context')

    formfield_overrides = psrformfield


# class ImageResource(resources.ModelResource):
#     class Meta:
#         model = Image
#
#
# class ImageAdmin(admin.ModelAdmin):
#     model = Image
#     resource_class = ImageResource
#     list_display = ('locality', 'occurrence_id')
#     fields = ('locality', 'occurrence', 'image')


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
#admin.site.register(Taxon, projects.admin.TaxonomyAdmin)
# admin.site.register(Image, ImageAdmin)
