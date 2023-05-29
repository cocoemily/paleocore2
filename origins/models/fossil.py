from django.contrib.gis.db import models
from django.utils.html import format_html
import uuid
from origins.ontologies import CONTINENT_CHOICES, TYPE_CHOICES, \
    VERIFIER_CHOICES, ANATOMICAL_REGION_CHOICES, ANATOMICAL_PRESERVATION_CHOICES

from django_countries.fields import CountryField
import publications
import projects.models
from ckeditor.fields import RichTextField as CKRichTextField


class Fossil(projects.models.PaleoCoreGeomBaseClass):
    """
    From projects.models.PaleoCoreBaseClass inherits:
    attributes: name, date_created, date_last_modified, problem, problem_comment, remarks, last_import
    methods: get_app_label, get_concrete_field_names, get_all_field_names, get_foreign_key_field_names, photo, thumbnail

    From projects.models.PaleoCoreGeomBaseClass inherits:
    attributes: georeference_remarks, geom, objects
    methods: gcs_coordinates, utm_coordinates, point_x, point_y, longitude, latitude, easting, northing
    """
    # Foreign keys
    context = models.ForeignKey(to='Context', on_delete=models.CASCADE, null=True, blank=True)

    # Fossil(Find) Fields
    guid = models.URLField(null=True, blank=True)  # The globally unique identifier for a fossil specimen
    uuid = models.UUIDField(default=uuid.uuid4)  # The universally unique identifier for a fossil speicmen
    # catalog_number provides the full catalog number as formatted in the first publication, including suffixes
    catalog_number = models.CharField(max_length=40, null=True, blank=True)
    # The lettered suffix for multipart specimens
    item_part = models.CharField(max_length=255, null=True, blank=True)
    # suffix_added tracks whether a suffix was added by Paleo Core / Origins team
    # A value of False indicates item_part/suffix was assigned by original team and appears in publication
    # A value of True indicates the item_part/suffix was assigned by Paleo Core / Origins team
    suffix_added = models.BooleanField(null=True)
    # other_catalog_number lists alternative typographic versions of the catalog number
    # e.g. OH 7 | O.H. 7 | OH-7 etc,
    other_catalog_numbers = models.CharField(max_length=255, null=True, blank=True)
    # The full date of discovery, where known
    date_discovered = models.DateField(null=True, blank=True)
    # TODO change year_collected to year_discovered or just migrate to date_discovered
    # The year the fossil was discovered or collected. Not distinction made.
    year_collected = models.IntegerField('Year', blank=True, null=True,
                                         help_text='The year, event or field campaign during which the item was found.')
    # The identifier for the organism the fossil is a part of. Portions of a skeleton will have separate catalog numbers
    # and share a common organism id. For example fossil A.L. 288-1a has organism_id A.L. 288-1
    organism_id = models.CharField(max_length=40, null=True, blank=True)
    # The nickname or popular name of the fossils, e.g. 'Selam', 'Tumai', 'Twiggy'
    nickname = models.CharField(max_length=40, null=True, blank=True)
    # Boolean field indicating if a fossil is a type specimen for any nomen.
    # The related nomina and their type statuses are given by the type_status() method.
    is_type_specimen = models.BooleanField('Type specimen', default=False)
    lifestage = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    short_description = CKRichTextField(null=True, blank=True)
    description = CKRichTextField(null=True, blank=True)

    # Taxon Fields
    taxon = models.ForeignKey('Taxon', null=True, blank=True, on_delete=models.SET_NULL)
    ttaxon = models.ForeignKey('TTaxon', null=True, blank=True, on_delete=models.SET_NULL)

    # Project Fields
    project_name = models.CharField(max_length=100, null=True, blank=True)
    project_abbreviation = models.CharField(max_length=10, null=True, blank=True)
    collection_code = models.CharField(max_length=10, null=True, blank=True)
    # NAAN is the name assigning authority number, often the shoulder of the guid
    naan = models.CharField(max_length=10, null=True, blank=True)
    # discovere_by refers to the person or agent that first located the fossil
    discovered_by = models.CharField(max_length=255, null=True, blank=True)
    # collected by refers to the person or agent that collected the fossil and is responsible for its sci. documtn.
    collected_by = models.CharField(max_length=255, null=True, blank=True)  # The person or agent that collected the

    # Location Fields
    place_name = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    site = models.ForeignKey('Site', on_delete=models.SET_NULL, null=True, blank=True)
    country = CountryField('Country', blank=True, null=True)
    continent = models.CharField(max_length=20, null=True, blank=True, choices=CONTINENT_CHOICES)
    # geom inherited from PC_Geom_Base class

    # Media Fields
    image = models.ImageField(max_length=255, blank=True, upload_to="uploads/images/origins", null=True)

    # Record Fields
    source = models.CharField(max_length=100, null=True, blank=True)
    #created_by = models.CharField(max_length=100, null=True, blank=True)
    #created = models.DateTimeField('Modified', auto_now_add=True)
    #modified = models.DateTimeField('Modified', auto_now=True,
    #                               help_text='The date and time this resource was last altered.')

    # Search and Filter Fields
    origins = models.BooleanField(default=False)  # in scope for origins project
    vif = models.BooleanField(default=False)  # very important fossil

    # Original Fields from Human Origins Program DB
    verbatim_PlaceName = models.CharField(max_length=100, null=True, blank=True)
    verbatim_HomininElement = models.CharField(max_length=40, null=True, blank=True)
    verbatim_HomininElementNotes = models.TextField(null=True, blank=True)
    verbatim_SkeletalElement = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementSubUnit = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementSubUnitDescriptor = models.CharField(max_length=100, null=True, blank=True)
    verbatim_SkeletalElementSide = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementPosition = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementComplete = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementClass = models.CharField(max_length=40, null=True, blank=True)
    verbatim_Locality = models.CharField(max_length=40, null=True, blank=True)
    verbatim_Country = models.CharField(max_length=20, null=True, blank=True)
    verbatim_provenience = models.TextField(null=True, blank=True)

    # References
    references = models.ManyToManyField(publications.models.Publication, blank=True)

    # Fields to manage data entry
    assigned_to = models.CharField('Assigned', max_length=255, null=True, blank=True, choices=VERIFIER_CHOICES)
    verified_by = models.CharField('Verified', max_length=255, null=True, blank=True, choices=VERIFIER_CHOICES)
    verified_date = models.DateField(null=True, blank=True)  # used to control visibility on nomen detail page

    # Helper field for managing Turkana imports
    to_split = models.BooleanField(null=True)

    def __str__(self):
        return str(self.catalog_number)

    def element_count(self):
        return FossilElement.objects.filter(fossil=self.id).count()

    def elements(self):
        """
        function to get a queryset of all skeletal elements associated with a fossil
        :return:
        """
        return self.fossil_element.all()

    def element_description(self):
        """
        function to get a text description of all skeletal elements associated with a fossil
        :return:
        """
        return ', '.join(["{} {}".format(e.skeletal_element_side, e.skeletal_element) for e in self.elements()])

    def default_image(self):
        """
        Function to fetch a default thumbnail image for a fossil
        :return:
        """
        images = self.photo_set.filter(default_image=True)
        if images.count() >= 1:
            return images[0].thumbnail()
        else:
            return None

    def get_subtype(self):
        """
        Determine if a Fossil instance has a subtype instance and if so what it is.
        :return: Returns a list of the matching subtype class or classes. Should never be more than one.
        """
        result = []
        try:
            TurkFossil.objects.get(pk=self.id)
            result.append(TurkFossil)
        except TurkFossil.DoesNotExist:
            pass
        return result

    def type_status(self, result_format='html'):
        """
        Get the type status (e.g. holotype, lectotype etc.) for every nomen that the fossil is a type of, or if not
        a type specimen return None
        :return:
        """
        result_string = ""
        # get all species-group nomina associated with this fossil, i.e. for which the fossil is a type specimen
        species_nomina_qs = self.nomen_set.filter(taxon_rank_group='species-group')
        if species_nomina_qs:
            if result_format == 'html':
                result_string = '<br/> '.join([f'<i>{n.name}</i>: {n.type_specimen_status}' for n in species_nomina_qs])
                result_string = format_html(result_string)
            elif result_format == 'txt':
                result_string = '; '.join(f'{n.name}: {n.type_specimen_status}' for n in species_nomina_qs)
        return result_string

    default_image.short_description = 'Fossil Thumbnail'
    default_image.allow_tags = True
    default_image.mark_safe = True


class FossilElement(models.Model):
    # Records
    source = models.CharField(max_length=100, null=True, blank=True)
    # Human Origins Program DB fields
    verbatim_PlaceName = models.CharField(max_length=100, null=True, blank=True)
    verbatim_HomininElement = models.CharField(max_length=40, null=True, blank=True)
    verbatim_HomininElementNotes = models.TextField(null=True, blank=True)
    verbatim_SkeletalElement = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementSubUnit = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementSubUnitDescriptor = models.CharField(max_length=100, null=True, blank=True)
    verbatim_SkeletalElementSide = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementPosition = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementComplete = models.CharField(max_length=40, null=True, blank=True)
    verbatim_SkeletalElementClass = models.CharField(max_length=40, null=True, blank=True)
    verbatim_Locality = models.CharField(max_length=40, null=True, blank=True)
    verbatim_Country = models.CharField(max_length=20, null=True, blank=True)

    # added fields
    hominin_element = models.CharField(max_length=40, null=True, blank=True)
    hominin_element_notes = models.TextField(null=True, blank=True)
    skeletal_element = models.CharField(max_length=40, null=True, blank=True)
    skeletal_element_subunit = models.CharField(max_length=40, null=True, blank=True)
    skeletal_element_subunit_descriptor = models.CharField(max_length=100, null=True, blank=True)
    skeletal_element_side = models.CharField(max_length=40, null=True, blank=True)
    skeletal_element_position = models.CharField(max_length=40, null=True, blank=True)
    skeletal_element_complete = models.CharField(max_length=40, null=True, blank=True)
    skeletal_element_class = models.CharField(max_length=40, null=True, blank=True)
    continent = models.CharField(max_length=20, null=True, blank=True)

    # Uberon fields
    uberon_id = models.CharField(max_length=100, null=True, blank=True)
    anatomical_region = models.CharField(max_length=100, null=True, blank=True, choices=ANATOMICAL_REGION_CHOICES)
    side = models.CharField(max_length=100, null=True, blank=True)
    dental = models.BooleanField(null=True, blank=True)
    completeness = models.CharField(max_length=100, null=True, blank=True, choices=ANATOMICAL_PRESERVATION_CHOICES)
    preserved_part = models.CharField(max_length=255, null=True, blank=True)

    # foreign keys
    fossil = models.ForeignKey(Fossil, on_delete=models.CASCADE, null=True, blank=False, related_name='fossil_element')

    def __str__(self):
        unicode_string = '['+str(self.id)+']'
        if self.skeletal_element_side:
            unicode_string = unicode_string+' '+self.skeletal_element_side
        if self.skeletal_element:
            unicode_string = unicode_string + ' ' + self.skeletal_element
        return unicode_string


class TurkFossil(Fossil):
    """Fossil occurrences imported from the Turkana Catalog compiled by F. Marchal and S. Prat"""
    verbatim_inventory_number = models.CharField(max_length=256, null=True, blank=True)  # = catalog_number
    verbatim_suffix = models.CharField(max_length=256, null=True, blank=True)  # add
    verbatim_year_discovered = models.CharField(max_length=256, null=True, blank=True)  # = year_collected
    verbatim_year_mentioned = models.CharField(max_length=256, null=True, blank=True)  # add
    verbatim_year_published = models.CharField(max_length=256, null=True, blank=True)
    verbatim_country = models.CharField(max_length=256, null=True, blank=True)  # = country
    verbatim_zone = models.CharField(max_length=256, null=True, blank=True)  # add
    verbatim_area = models.CharField(max_length=256, null=True, blank=True)  # add
    verbatim_locality = models.CharField(max_length=256, null=True, blank=True)  # = locality
    verbatim_formation = models.CharField(max_length=256, null=True, blank=True)  # = formation
    verbatim_member = models.CharField(max_length=256, null=True, blank=True)  # = member
    verbatim_level = models.CharField(max_length=256, null=True, blank=True)  # = bed
    verbatim_age_g1 = models.CharField(max_length=256, null=True, blank=True)  # = context__best_age
    verbatim_age_g2 = models.CharField(max_length=256, null=True, blank=True)  #
    verbatim_anatomical_part = models.CharField(max_length=256, null=True, blank=True)  # =
    verbatim_anatomical_description = models.CharField(max_length=256, null=True, blank=True)
    verbatim_taxonomy1 = models.CharField(max_length=256, null=True, blank=True)
    verbatim_taxonomy2 = models.CharField(max_length=256, null=True, blank=True)
    verbatim_robusticity = models.CharField(max_length=256, null=True, blank=True)
    verbatim_finder = models.CharField(max_length=256, null=True, blank=True)  # = discovered_by
    verbatim_reference_first_mention = models.CharField(max_length=256, null=True, blank=True)
    verbatim_reference_description = models.CharField(max_length=256, null=True, blank=True)
    verbatim_reference_identification = models.CharField(max_length=256, null=True, blank=True)
    verbatim_reference_dating = models.CharField(max_length=256, null=True, blank=True)
    region = models.CharField(max_length=256, null=True, blank=True)
    suffix_assigned = models.BooleanField(null=True)
    in_origins = models.BooleanField(null=True)
    to_add = models.BooleanField(null=True)
    to_divide = models.BooleanField(null=True)

