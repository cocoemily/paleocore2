from django.contrib import admin
import origins.models
import origins.util
import origins.ontologies
from projects.admin import PaleoCoreLocalityAdminGoogle, TaxonomyAdmin
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.urls import reverse
import origins.views
from django.contrib import messages
from django.contrib.gis.geos import Point

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'reference_no', 'author1last', 'reftitle']
    search_fields = ['reference_no', 'author1init', 'author1last', 'author2init', 'author2last',
                     'otherauthors', 'pubyr', 'reftitle', 'pubtitle', 'editors', 'pubvol', 'publication_type']
    list_filter = ['publication_type']
    list_per_page = 200


class ReferenceInline(admin.TabularInline):
    model = origins.models.Reference.fossil.through
    extra = 1


class ContextPublicationsInline(admin.TabularInline):
    model = origins.models.Context.references.through
    extra = 1
    verbose_name = "Publication"
    verbose_name_plural = "Publications"


class ContextInline(admin.TabularInline):
    model = origins.models.Context


class SitePublicationsInline(admin.TabularInline):
    model = origins.models.Site.references.through
    extra = 1
    verbose_name = "Publication"
    verbose_name_plural = "Publications"


class SiteResource(resources.ModelResource):
    class Meta:
        model = origins.models.Site


class SiteAdmin(PaleoCoreLocalityAdminGoogle):
    save_as = True
    list_display = ['id', 'name', 'country', 'problem',
                    # 'verbatim_collection_name',
                    # 'longitude', 'latitude',
                    # 'verbatim_early_interval',
                    # 'verbatim_late_interval',
                    'max_ma',
                    'min_ma',
                    'fossil_count',
                    'formation',
                    'verbatim_collection_name',
                    # 'context_usages',
                    # 'verbatim_reference_no',
                    # 'origins'
                    ]
    # list_editable = ['name', 'origins']
    readonly_fields = ['latitude', 'longitude', 'fossil_usages', 'context_usages']
    search_fields = ['id', 'name', 'alternate_names', 'country', 'verbatim_collection_name',
                     'verbatim_early_interval',
                     'verbatim_late_interval',
                     'verbatim_max_ma',
                     'verbatim_min_ma',
                     'verbatim_reference_no',
                     'origins'
                     ]
    list_filter = ['origins', 'country', 'problem']
    list_per_page = 500
    inlines = [SitePublicationsInline]

    fieldsets = [
        ('Occurrence Details', {
            'fields': [('name',), ('alternate_names',), ('origins',), ('remarks',)],
        }),
        ('Geological Context', {
            'fields': [('min_ma', 'max_ma'), ('formation',)]
        }),
        ('Verbatim', {
            'fields': ['source', 'verbatim_collection_no', 'verbatim_record_type', 'verbatim_formation',
                       'verbatim_lng', 'verbatim_lat', 'verbatim_collection_name', 'verbatim_collection_subset',
                       'verbatim_collection_aka', 'verbatim_n_occs', 'verbatim_early_interval',
                       'verbatim_late_interval', 'verbatim_max_ma', 'verbatim_min_ma', 'verbatim_reference_no'],
            'classes': ['collapse'],
        }),
        ('Location', {
            'fields': [('country', ), ('location_remarks', ), ('latitude', 'longitude'), ('geom',)]
        }),
        ('Administration', {
             'fields': [('problem', 'problem_comment',)]
         }),

    ]


class ActiveSiteAdmin(SiteAdmin, ImportExportActionModelAdmin):
    resource_class = SiteResource
    list_display = ['id', 'name', 'country', 'max_ma', 'min_ma', 'fossil_count', 'formation',
                    'verbatim_collection_name']

    def get_queryset(self, request):
        return origins.models.Site.objects.filter(origins=True)


class ContextAdmin(PaleoCoreLocalityAdminGoogle):
    save_as = True
    list_display = ['id', 'name', 'site_link', 'geological_formation', 'geological_member',
                    'max_stage', 'min_stage', 'max_age', 'min_age', 'best_age']
    search_fields = ['id', 'name', 'geological_formation', 'geological_member',
                     'max_stage', 'min_stage', 'max_epoch', 'min_epoch', 'max_period', 'min_period',
                     'older_interval', 'younger_interval', 'max_age', 'min_age', 'best_age']
    list_filter = ['origins', 'site__name']
    list_per_page = 500
    fieldsets = [
        ('Context Details', {
            'fields': [('name', 'origins', 'source')],
        }),
        ('Stratigraphy', {
            'fields': [('geological_formation', 'geological_member',)],
        }),
        ('Chronostratigraphy', {
            'fields': [('max_period', 'min_period',),
                       ('max_epoch', 'min_epoch',),
                       ('max_stage', 'min_stage'),
                       ],
        }),
        ('Geochronology', {
            'fields': [('older_interval', 'younger_interval',),
                       ('max_age', 'min_age', 'best_age')],
        }),
        ('Location', {'fields': [('site',), ]}),
        ('Verbatim', {
            'fields': ['verbatim_collection_no', 'verbatim_record_type', 'verbatim_formation',
                       'verbatim_lng', 'verbatim_lat', 'verbatim_collection_name', 'verbatim_collection_subset',
                       'verbatim_collection_aka', 'verbatim_n_occs', 'verbatim_early_interval',
                       'verbatim_late_interval', 'verbatim_max_ma', 'verbatim_min_ma', 'verbatim_reference_no'],
            'classes': ['collapse'],
        }),
    ]
    inlines = [
        ContextPublicationsInline,
    ]
    actions = ['create_site_from_context']

    def site_link(self, obj):
        if obj.site:
            site_url = reverse('admin:origins_site_change', args=(obj.site.id,))
            return format_html('<a href={}>{}</a>'.format(site_url, obj.site))
        else:
            return None

    site_link.admin_order_field = 'context'
    site_link.short_description = 'Site'

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.current_obj = obj
        return super(ContextAdmin, self).get_form(request, obj, **kwargs)

    def create_site_from_context(self, request, queryset):
        def create_site(context):
            new_site = origins.models.Site()
            for key in new_site.get_concrete_field_names():
                try:
                    new_site.__dict__[key] = context.__dict__[key]
                except KeyError:
                    pass
            if new_site.verbatim_lat and new_site.verbatim_lng:
                new_site.geom = Point(float(new_site.verbatim_lng), float(new_site.verbatim_lat))
                new_site.country = origins.util.get_country_from_geom(new_site.geom)
            new_site.save()
            return new_site

        obj_count = 0
        for obj in queryset:
            new_site_obj = create_site(obj)  # create a new site based on the data in the context
            obj.site = new_site_obj  # assign the newly created site to the context
            obj_count += 1
        if obj_count == 1:
            count_string = '1 record'
        if obj_count > 1:
            count_string = '{} records'.format(obj_count)
        messages.add_message(request, messages.INFO,
                             'Successfully updated {}'.format(count_string))
    create_site_from_context.short_description = 'Create Site object(s) from Context(s)'

    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     """
    #     Simplify choice list for sites to only those sites from the designated country.
    #     :param db_field:
    #     :param request:
    #     :param kwargs:
    #     :return:
    #     """
    #
    #     if db_field.name == "site":
    #         kwargs["queryset"] = Site.objects.filter(country=self.current_obj.country).filter(origins=True)
    #     return super(ContextAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class FossilElementInline(admin.TabularInline):
    model = origins.models.FossilElement
    fields = ['skeletal_element', 'skeletal_element_subunit', 'skeletal_element_subunit_descriptor',
              'skeletal_element_side', 'skeletal_element_position', 'skeletal_element_complete',
              'skeletal_element_class']
    extra = 0

class UberonElementInline(admin.TabularInline):
    model = origins.models.FossilElement
    fields = ['uberon_id', 'anatomical_region', 'side', 'dental', 'completeness', 'preserved_part']
    extra = 0

class PhotosInline(admin.StackedInline):
    model = origins.models.Photo
    extra = 0
    readonly_fields = ('thumbnail',)
    fieldsets = [
        ('Photos', {
            'fields': [('default_image', 'image', 'thumbnail', 'description')]})]


class FossilPublicationsInline(admin.TabularInline):
    model = origins.models.Fossil.references.through
    extra = 1
    verbose_name = "Publication"
    verbose_name_plural = "Publications"
    ordering = ["publication__year"]


class FossilAdmin(admin.ModelAdmin):
    list_display = ['id', 'catalog_number', 'is_type_specimen', 'site_link', 'context_link', 'taxon_link',
                    'country', 'context__best_age',
                    'short_description', 'vif', 'assigned_to', 'verified_by', 'verified_date',
                    'default_image', 'problem'
                    # 'element_description',
                    ]
    list_editable = ['vif']
    list_filter = ['origins',
                   'vif',
                   'is_type_specimen',
                   # 'type_status',
                   'assigned_to',
                   'verified_by',
                   'verified_date',
                   'source',
                   'site__name',
                   'country']
    list_display_links = ['id', 'catalog_number']
    list_select_related = ['site', 'context', 'taxon']
    search_fields = ['catalog_number', 'other_catalog_numbers', 'place_name', 'country', 'locality',
                     'fossil_element__skeletal_element']
    readonly_fields = ['element_count', 'id', 'default_image', 'element_description', 'taxon_link', 'type_status']
    save_as = True

    list_per_page = 200
    inlines = [
        # ReferenceInline, # the number of references significantly slows page loads
        FossilPublicationsInline,
        FossilElementInline,
        UberonElementInline,
        PhotosInline,
    ]
    filter_horizontal = ('references', )

    fieldsets = [
        ('Fossil Details', {
            'fields': [('id',),
                       ('catalog_number', 'organism_id'),
                       ('guid', ),
                       ('other_catalog_numbers', 'nickname'),
                       ('description',),
                       ('short_description',),
                       ('lifestage', 'sex'),
                       ('is_type_specimen',),
                       ('type_status',),
                       ('origins', 'vif')],
        }),

        ('Events', {
            'fields': [('date_discovered', 'discovered_by'),
                       ('year_collected', 'collected_by')]
        }),
        ('Taxon', {
            'fields': [('ttaxon',)]
        }),
        ('Location', {
            'fields': [
                ('continent', ),
                ('country', ),
                ('site', 'locality'),
                ('context',)
            ]
        }),
        ('Remarks', {
            'fields': [('remarks',), ]
        }),
        ('Validation', {
            'fields': [
                ('assigned_to', 'verified_by', 'verified_date',),
                ('date_created', 'date_last_modified',),
                ('problem',),
                ('problem_comment',),
            ],
        }),
        ('Verbatim', {
            'fields': [('verbatim_PlaceName', 'verbatim_HomininElement'),
                       ('verbatim_HomininElementNotes',),
                       ('verbatim_SkeletalElement', 'verbatim_SkeletalElementSubUnit',
                        'verbatim_SkeletalElementSubUnitDescriptor'),
                       ('verbatim_SkeletalElementSide',
                        'verbatim_SkeletalElementPosition', 'verbatim_SkeletalElementComplete',
                        'verbatim_SkeletalElementClass'),
                       ('verbatim_Locality', 'verbatim_Country'),
                       ],
            'classes': ['collapse'],
        }),
    ]

    actions = ['toggle_origins', 'update_sites']

    def context__formation(self, obj):
        """
        Function to get the formation from via the context
        :param obj:
        :return:
        """
        if obj.context:
            return obj.context.geological_formation
        else:
            return None

    context__formation.admin_order_field = 'context'
    context__formation.short_description = 'Geo formation'

    def context_link(self, obj):
        if obj.context:
            context_url = reverse('admin:origins_context_change', args=(obj.context.id,))
            return format_html('<a href={}>{}</a>'.format(context_url, obj.context))
        else:
            return None

    context_link.admin_order_field = 'context'
    context_link.short_description = 'Context'

    def site_link(self, obj):
        if obj.site:
            site_url = reverse('admin:origins_site_change', args=(obj.site.id,))
            return format_html('<a href={}>{}</a>'.format(site_url, obj.site))
        else:
            return None

    def taxon_link(self, obj):
        if obj.ttaxon:
            taxon_url = reverse('admin:origins_ttaxon_change', args=(obj.ttaxon.id,))
            return format_html('<a href={}>{}</a>'.format(taxon_url, obj.ttaxon))
        else:
            return None

    def context__site(self, obj):
        """
        Function to get site information via the context. Returns a link to the site change detail page.
        :param obj:
        :return:
        """
        if obj.context and obj.context.site:
            site_url = reverse('admin:origins_site_change', args=(obj.context.site.id,))
            return format_html('<a href={}>{}</a>'.format(site_url, obj.context.site))
        else:
            return None

    context__site.admin_order_field = 'context'
    context__site.short_description = 'Site'

    def context__max_age(self, obj):
        """
        Function to get age via context.
        :param obj:
        :return:
        """
        if obj.context and obj.context.max_age:
            return obj.context.max_age
        else:
            return None

    context__max_age.short_description = "Max age"

    def context__min_age(self, obj):
        """
        Function to get age via context.
        :param obj:
        :return:
        """
        if obj.context and obj.context.min_age:
            return obj.context.min_age
        else:
            return None

    context__min_age.short_description = "Min age"

    def context__best_age(self, obj):
        """
        Function to get age via context.
        :param obj:
        :return:
        """
        if obj.context and obj.context.best_age:
            return obj.context.best_age
        else:
            return None

    context__min_age.short_description = "Best age"

    def get_form(self, request, obj=None, **kwargs):
        self.current_obj = None
        if obj:
            self.current_obj = obj
        return super(FossilAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Simplify choice list for context to only those context objects occurring at the site.
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        # LBYL - Check if current form has an object selected. This prevents errors raised when using list editables.
        if hasattr(self, 'current_obj'):
            #  Line below checks if current object is not None. We need this check so that we can open blank forms for
            #  new entries.
            if db_field.name == "site" and self.current_obj:
                kwargs["queryset"] = origins.models.Site.objects.filter(country=self.current_obj.country).order_by('name')
            if db_field.name == "context" and self.current_obj:
                kwargs["queryset"] = origins.models.Context.objects.filter(site=self.current_obj.site).order_by('name')

        return super(FossilAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def update_sites(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        ids = '?ids={}'.format(','.join(selected))
        redirect_url = reverse('admin:update_sites')
        return HttpResponseRedirect(redirect_url + ids)

    def toggle_origins(modeladmin, request, queryset):
        for obj in queryset:
            obj.origins = not(obj.origins)
            obj.save()

    def change_xy(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        redirect_url = reverse("admin:change_xy")
        return HttpResponseRedirect(redirect_url + "?ids=%s" % (",".join(selected)))
    change_xy.short_description = "Manually change coordinates for a point"

    # Add to the admin urls
    def get_urls(self):
        return [
                   # url(r'^update_sites/(?P<ids>)/$',
                   url(r'^update_sites/$',
                       permission_required('origins.update_sites', login_url='login/')(
                           origins.views.UpdateSites.as_view()),
                       name="update_sites"),
               ] + super(FossilAdmin, self).get_urls()


class TaxonPublicationsInline(admin.TabularInline):
    model = origins.models.Taxon.references.through
    extra = 1
    verbose_name = "Publication"
    verbose_name_plural = "Publications"


class TaxonAdmin(TaxonomyAdmin):
    fields = TaxonomyAdmin.fields
    inlines = [TaxonPublicationsInline]


class TTaxonPublicationsInline(admin.TabularInline):
    model = origins.models.TTaxon.references.through
    extra = 1
    verbose_name = "Publication"
    verbose_name_plural = "Publications"


class TTaxonAdmin(MPTTModelAdmin, TaxonomyAdmin):
    readonly_fields = ['id', 'scientific_name', '_synonyms',
                       'nomenclatural_status', 'nomenclatural_code', 'taxon_epithet',
                       'biology_usages', 'fossil_usages', 'year', 'nomen_link' ]
    list_display = ['name','nomen_link', 'scientific_name', 'rank', 'classification_status', 'nomenclatural_status',
                    'fossil_usages', '_synonyms']
    fields = ['id', 'name','nomen', 'abbreviation', 'rank', 'parent', 'classification_status', 'junior_to',
              'nomenclatural_status', 'nomenclatural_code',
              'biology_usages','fossil_usages',
              'scientific_name', '_synonyms', 'year',
              'remarks',]
    inlines = [TTaxonPublicationsInline]
    list_filter = ['classification_status', 'rank']
    save_as = True

    def nomen_link(self, obj):
        if obj.nomen:
            nomen_url = reverse('admin:origins_nomen_change', args=(obj.nomen.id,))
            return format_html('<a href={}>{}</a>'.format(nomen_url, obj.nomen))
        else:
            return None

class NomenPublicationsInline(admin.TabularInline):
    model = origins.models.Nomen.references.through
    extra = 1
    verbose_name = "Publication"
    verbose_name_plural = "Publications"


class NomenAdmin(admin.ModelAdmin):
    readonly_fields = ['scientific_name', 'scientific_name_html', 'full_name_html', 'authorship_reference',
                       'authorship_year', 'authorship_reference_id', 'taxon_rank_label']
    list_display = ['name', 'authorship', 'year', 'authorship_reference_obj', 'type_specimen',
                    'taxon_rank_obj', 'is_objective_synonym', 'is_subjective_synonym', 'is_available', 'is_established',
                    'is_potentially_valid', 'nomenclatural_status', 'status_remark',
                    'problem', 'is_inquirenda',
                    'assigned_to', 'verified_by', 'verified_date']
    list_editable = ['status_remark', 'is_inquirenda']
    list_filter = ['nomenclatural_status', 'status_remark', 'taxon_rank_obj', 'assigned_to', 'verified_by',
                   'verified_date',
                   'is_available', 'is_potentially_valid', 'is_established',
                   'is_objective_synonym', 'is_subjective_synonym', 'bc_status', 'problem', 'is_inquirenda',
                   'is_chibanian']
    inlines = [NomenPublicationsInline]
    search_fields = ['name', 'authorship', 'year', 'remarks', 'usage_remarks', 'problem_comment']
    fieldsets = [
        ('Nomen Details', {
            'fields': [
                ('name', 'scientific_name_id'),
                ('generic_name', 'specific_epithet',)
            ],
        }),
        ('Authorship', {
            'fields': [
                ('authorship', 'year'),
                ('authorship_reference_obj',),
                ('authorship_reference',),
                ('authorship_reference_id',),
            ],
        }),
        ('Taxon Rank', {
            'fields': [
                ('taxon_rank_obj',),
                ('taxon_rank_label',),
                ('taxon_rank_group',),
            ],
        }),
        ('Type Specimen', {
            'fields': [('type_specimen_label',),
                       ('type_specimen', 'type_specimen_status'),
                       ('paratypes',),
                       ('type_taxon',),
                       ],
        }),
        ('Nomenclatural Status', {
            'fields': [
                ('nomenclatural_status', 'nomenclatural_code',),
                ('is_available',),
                ('is_potentially_valid',),
                ('is_established',),
                ('is_objective_synonym',),
                ('is_subjective_synonym',),
                ('is_inquirenda',),
                ('is_chibanian',),
                ('status_remark',),
            ]
        }),
        ('Remarks', {
            'fields': [
                ('bc_status',),
                ('remarks',),
                ('usage_remarks',),

            ],
        }),
        ('Validation', {
            'fields': [
                ('assigned_to', 'verified_by', 'verified_date',),
                ('date_created', 'date_last_modified',),
                ('problem',),
                ('problem_comment',),
            ],
        }),
    ]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Simplify choice list for type_object to only those context objects occurring at the site.
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        if db_field.name == "type_specimen":
            kwargs["queryset"] = origins.models.Fossil.objects.filter(is_type_specimen=True).order_by('catalog_number')

        return super(NomenAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ActiveNomenAdmin(NomenAdmin):
    # Get the queryset of active nomen
    def get_queryset(self, request):
        species_rank = origins.models.TaxonRank.objects.get(ordinal=70)
        qs = origins.models.Nomen.objects.filter(is_objective_synonym=False).filter(is_subjective_synonym=False)
        qs = qs.filter(nomenclatural_status=origins.ontologies.potentially_valid).filter(taxon_rank_obj=species_rank)
        return qs


class TurkFossilAdmin(FossilAdmin):
    def get_fieldsets(self, request, obj=None):
        """
        Dynamically revise verbatim section of admin form for Turkana Fossils.
        :param request:
        :param obj:
        :return: updated list of field sets
        """
        # Define a new verbatim fieldset for Turkana Fossils
        turkana_verbatim_fieldset = ['Verbatim', {
            'fields': [('verbatim_inventory_number', 'verbatim_suffix'),
                       ('verbatim_year_discovered', 'verbatim_year_mentioned', 'verbatim_year_published'),
                       ('verbatim_country',),
                       ('verbatim_zone', 'verbatim_area', 'verbatim_locality'),
                       ('verbatim_formation', 'verbatim_member', 'verbatim_level'),
                       ('verbatim_age_g1', 'verbatim_age_g2'),
                       ('verbatim_anatomical_part',),
                       ('verbatim_anatomical_description',),
                       ('verbatim_taxonomy1', 'verbatim_taxonomy2'),
                       ('verbatim_robusticity',),
                       ('verbatim_finder',),
                       ('verbatim_reference_first_mention',),
                       ('verbatim_reference_description',),
                       ('verbatim_reference_identification',),
                       ('verbatim_reference_dating',),
                       ('region',),
                       ('suffix_assigned',),
                       ('in_origins',),
                       ('to_add',),
                       ('to_divide',),
                       ],
            'classes': ['collapse'],
        }],
        fieldsets = super(TurkFossilAdmin, self).get_fieldsets(request, obj)
        # Check that the final fieldset is called Verbatim and if so replace it.
        if fieldsets[-1][0]=='Verbatim':
            fieldsets = list(fieldsets[:-1])+list(turkana_verbatim_fieldset)
        return fieldsets
    list_display = ['id', 'catalog_number', 'is_type_specimen', 'site_link', 'context_link', 'taxon_link',
                    'country', 'context__best_age','verbatim_age_g1', 'verbatim_age_g2', 'region',
                    'verbatim_zone', 'verbatim_area', 'verbatim_locality','default_image', 'vif', 'problem'
                    ]
    list_filter = ['problem','vif', 'is_type_specimen','region', 'verbatim_zone', 'suffix_assigned', 'in_origins']
    change_list_template = "admin/top_pagination_change_list.html"
    list_per_page = 100


class SkeletalElementAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'uberon_id', 'anatomical_region']
    list_filter = ['anatomical_region',]
    search_fields = ['name', 'uberon_id', 'anatomical_region']
    list_per_page = 300

# Register your models here.
admin.site.register(origins.models.Context, ContextAdmin)
admin.site.register(origins.models.Reference, ReferenceAdmin)
admin.site.register(origins.models.Fossil, FossilAdmin)
admin.site.register(origins.models.Site, ActiveSiteAdmin)
admin.site.register(origins.models.TTaxon, TTaxonAdmin)
admin.site.register(origins.models.TaxonRank)
admin.site.register(origins.models.Nomen, NomenAdmin)
admin.site.register(origins.models.ActiveNomen, ActiveNomenAdmin)
admin.site.register(origins.models.TurkFossil, TurkFossilAdmin)
admin.site.register(origins.models.SkeletalElement, SkeletalElementAdmin)
