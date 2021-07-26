from django.contrib.gis.db import models
#import origins.models
#from origins.models import Site, Context, TTaxon, Taxon
import uuid
from origins.ontologies import CONTINENT_CHOICES, NOMENCLATURAL_STATUS_CHOICES, NOMENCLATURAL_CODE_CHOICES, TYPE_CHOICES, \
    CLASSIFICATION_STATUS_CHOICES
from django_countries.fields import CountryField
import publications


class Fossil(models.Model):
    # Foreign keys
    context = models.ForeignKey(to='Context', on_delete=models.CASCADE, null=True, blank=True)

    # Fossil(Find)
    guid = models.URLField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    # catalog_number provides the full catalog number as formatted in the first publication, including suffixes
    catalog_number = models.CharField(max_length=40, null=True, blank=True)
    # other_catalog_number lists alternative typographic versions of the catalog number
    # e.g. OH 7 | O.H. 7 | OH-7 etc,
    other_catalog_numbers = models.CharField(max_length=255, null=True, blank=True)
    date_discovered = models.DateField(null=True, blank=True)
    # TODO change year_collected to year_discovered or just migrate to date_discovered
    year_collected = models.IntegerField('Year', blank=True, null=True,
                                         help_text='The year, event or field campaign during which the item was found.')
    organism_id = models.CharField(max_length=40, null=True, blank=True)
    nickname = models.CharField(max_length=40, null=True, blank=True)
    is_type_specimen = models.BooleanField('Type Specimen', default=False)
    type_status = models.CharField(max_length=255, null=True, blank=True, choices=TYPE_CHOICES)
    lifestage = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    # Taxon
    taxon = models.ForeignKey('Taxon', null=True, blank=True, on_delete=models.SET_NULL)
    ttaxon = models.ForeignKey('TTaxon', null=True, blank=True, on_delete=models.SET_NULL)

    # Project
    project_name = models.CharField(max_length=100, null=True, blank=True)
    project_abbreviation = models.CharField(max_length=10, null=True, blank=True)
    collection_code = models.CharField(max_length=10, null=True, blank=True)
    # NAAN is the name assigning authority number, often the shoulder of the guid
    naan = models.CharField(max_length=10, null=True, blank=True)
    # discovere_by refers to the person or agent that first located the fossil
    discovered_by = models.CharField(max_length=255, null=True, blank=True)
    # collected by refers to the person or agent that collected the fossil and is responsible for its sci. documtn.
    collected_by = models.CharField(max_length=255, null=True, blank=True)  # The person or agent that collected the

    # Location
    place_name = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=40, null=True, blank=True)
    site = models.ForeignKey('Site', on_delete=models.SET_NULL, null=True, blank=True)
    # country = models.CharField(max_length=10, null=True, blank=True)
    country = CountryField('Country', blank=True, null=True)
    continent = models.CharField(max_length=20, null=True, blank=True, choices=CONTINENT_CHOICES)
    geom = models.PointField(null=True, blank=True)

    # Media
    image = models.ImageField(max_length=255, blank=True, upload_to="uploads/images/origins", null=True)

    # Record
    source = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField('Modified', auto_now_add=True)
    modified = models.DateTimeField('Modified', auto_now=True,
                                    help_text='The date and time this resource was last altered.')

    # Search and Filter Fields
    origins = models.BooleanField(default=False)  # in scope for origins project

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

    default_image.short_description = 'Fossil Thumbnail'
    default_image.allow_tags = True
    default_image.mark_safe = True

    def aapa(self):
        """
        Method to indicate if fossil belowns in analysis set for AAPA 2017.
        Returns true if the fossil comes from a mio-pliocene locality in Africa
        :return: True or False
        """
        young_sites = [None, 'Olduvai', 'Border Cave', 'Lincoln Cave', 'Olorgesailie', 'Klasies River',
                       'Thomas Quarries', u'Sal\xe9', u'Haua Fteah', u'Melka-Kuntur\xe9 (cf. Locality)',
                       u'Olduvai Gorge', u'Cave of Hearths', u'Kanjera (Locality)']
        return self.continent == 'Africa' and self.locality not in young_sites


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
    side = models.CharField(max_length=100, null=True, blank=True)

    # foreign keys
    fossil = models.ForeignKey(Fossil, on_delete=models.CASCADE, null=True, blank=False, related_name='fossil_element')

    def __str__(self):
        unicode_string = '['+str(self.id)+']'
        if self.skeletal_element_side:
            unicode_string = unicode_string+' '+self.skeletal_element_side
        if self.skeletal_element:
            unicode_string = unicode_string + ' ' + self.skeletal_element
        return unicode_string


class TurkanaFossil(models.Model):
    verbatim_catalog_number = models.CharField(max_length=256, null=True, blank=True)
    verbatim_suffix = models.CharField(max_length=256, null=True, blank=True)
    catalog_number = models.CharField(max_length=256, null=True, blank=True)
    collection_code = models.CharField(max_length=256, null=True, blank=True)
    specimen_number = models.IntegerField(null=True, blank=True)
    specimen_suffix = models.CharField(max_length=256, null=True, blank=True)
    region = models.CharField(max_length=256, null=True, blank=True)
    suffix_assigned = models.BooleanField(null=True)
    in_origins = models.BooleanField(null=True)
    in_turkana = models.BooleanField(null=True)
