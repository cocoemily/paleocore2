# Python imports
import os
import uuid
# Django imports
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType

from django.utils.html import mark_safe, format_html
# Django countries imports
from django_countries.fields import CountryField
# Wagtail imports
#from wagtail.core.models import Page, Orderable
#from taggit.models import TaggedItemBase
#from utils.models import RelatedLink, CarouselItem
# Paleo Core imports
import projects.models
import publications.models
from .ontologies import CONTINENT_CHOICES, NOMENCLATURAL_STATUS_CHOICES, NOMENCLATURAL_CODE_CHOICES
import publications.models

from mptt.models import MPTTModel, TreeForeignKey


# Taxonomy models inherited from paleo core base project
class TaxonRank(projects.models.TaxonRank):
    class Meta:
        verbose_name = "Taxon Rank"
        ordering = ['ordinal']


class Taxon(projects.models.Taxon):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    rank = models.ForeignKey('TaxonRank', null=True, blank=True, on_delete=models.SET_NULL)
    references = models.ManyToManyField(publications.models.Publication, blank=True)

    class Meta:
        verbose_name = "Taxon"
        verbose_name_plural = "Taxa"
        ordering = ['rank__ordinal', 'label']


class IdentificationQualifier(projects.models.IdentificationQualifier):
    class Meta:
        verbose_name = "Identification Qualifier"


class TTaxon(MPTTModel, projects.models.Taxon):
    """
    Modified Preordered Tree Traversal Taxon class
    """
    epithet = models.CharField(max_length=255, null=True, blank=True)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)
    authorship = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    nomenclatural_code = models.CharField(max_length=255, null=True, blank=True, default='ICZN',
                                          choices=NOMENCLATURAL_CODE_CHOICES)
    nomenclatural_status = models.CharField(max_length=255, null=True, blank=True, choices=NOMENCLATURAL_STATUS_CHOICES)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    junior_to = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='synonyms')
    rank = models.ForeignKey('TaxonRank', null=True, blank=True, on_delete=models.SET_NULL)
    references = models.ManyToManyField(publications.models.Publication, blank=True)

    def fossil_usages(self):
        """
        Count the number of Fossil objects pointing to the ttaxon instance. This method uses
        the content type system to find the containing app and model.
        :return: Returns and integer count of the number of biology instances in the app that point to the taxon.
        """
        result = None
        app = self._meta.app_label
        try:
            content_type = ContentType.objects.get(app_label=app, model='fossil')  # assumes the model is named Biology
            this_fossil_model = content_type.model_class()
            result = this_fossil_model.objects.filter(ttaxon=self).count()
        except ContentType.DoesNotExist:
            pass  # If no matching content type then we'll pass here and return None
        return result

    def scientific_name(self):
        """
        Generate pretty format html with full scientific name
        :return:
        """
        scientific_name_html = ''
        if self.authorship:
            scientific_name_html = '<i>' + self.name + '</i> ' + self.authorship
        else:
            scientific_name_html = '<i>' + self.name
        return format_html(scientific_name_html)

    class Meta:
        verbose_name = "TTaxon"
        verbose_name_plural = "TTaxa"
        ordering = ['rank__ordinal', 'label']

    class MPTTMeta:
        order_insertion_by = ['name']


class Reference(models.Model):
    # Original fields from Paleobiology DB
    reference_no = models.IntegerField(blank=True, null=True)
    record_type = models.CharField(max_length=5, null=True, blank=True)
    ref_type = models.CharField(max_length=201, null=True, blank=True)
    author1init = models.CharField(max_length=202, null=True, blank=True)
    author1last = models.CharField(max_length=203, null=True, blank=True)
    author2init = models.CharField(max_length=204, null=True, blank=True)
    author2last = models.CharField(max_length=205, null=True, blank=True)
    otherauthors = models.TextField(null=True, blank=True)
    pubyr = models.CharField(max_length=207, null=True, blank=True)
    reftitle = models.TextField(null=True, blank=True)
    pubtitle = models.TextField(null=True, blank=True)
    editors = models.TextField(null=True, blank=True)
    pubvol = models.CharField(max_length=210, null=True, blank=True)
    pubno = models.CharField(max_length=211, null=True, blank=True)
    firstpage = models.CharField(max_length=212, null=True, blank=True)
    lastpage = models.CharField(max_length=213, null=True, blank=True)
    publication_type = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=214, null=True, blank=True)
    doi = models.CharField(max_length=215, null=True, blank=True)
    # Added fields
    source = models.CharField(max_length=216, null=True, blank=True)
    fossil = models.ManyToManyField(to='Fossil')
    # Media
    reference_pdf = models.FileField(max_length=255, blank=True, upload_to="uploads/files/origins", null=True)

    def __str__(self):
        unicode_string = '['+str(self.id)+']'
        if self.author1last:
            unicode_string = unicode_string+' '+self.author1last
        elif self.pubyr:
            unicode_string = unicode_string+' '+str(self.pubyr)
        return unicode_string

    def get_concrete_field_names(self):
        """
        Get field names that correspond to columns in the DB
        :return: returns a lift
        """
        field_list = self._meta.get_fields()
        return [f.name for f in field_list if f.concrete]


class Site(projects.models.PaleoCoreSiteBaseClass):
    """
    Inherits country,
    """
    name = models.CharField("Site Name", max_length=40, null=True, blank=True)
    alternate_names = models.TextField(null=True, blank=True)
    min_ma = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    max_ma = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    formation = models.CharField(max_length=50, null=True, blank=True)

    # Location
    # country = CountryField('Country', blank=True, null=True)
    geom = models.PointField(srid=4326, null=True, blank=True)
    location_remarks = models.TextField(null=True, blank=True)

    # Filter and Search
    origins = models.BooleanField(default=False)  # in scope for origins project

    # Original fields from Paleobiology DB
    source = models.CharField(max_length=20, null=True, blank=True)
    verbatim_collection_no = models.IntegerField(blank=True, null=True)
    verbatim_record_type = models.CharField(max_length=20, null=True, blank=True)
    verbatim_formation = models.CharField(max_length=50, null=True, blank=True)
    verbatim_lng = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    verbatim_lat = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    verbatim_collection_name = models.CharField(max_length=200, null=True, blank=True)
    verbatim_collection_subset = models.CharField(max_length=20, null=True, blank=True)
    verbatim_collection_aka = models.CharField(max_length=200, null=True, blank=True)
    verbatim_n_occs = models.IntegerField(null=True, blank=True)
    verbatim_early_interval = models.CharField(max_length=50, null=True, blank=True)
    verbatim_late_interval = models.CharField(max_length=50, null=True, blank=True)
    verbatim_max_ma = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    verbatim_min_ma = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    verbatim_reference_no = models.IntegerField(null=True, blank=True)

    # Calculated Fields
    fossil_count = models.IntegerField(null=True, blank=True)

    # References
    references = models.ManyToManyField(publications.models.Publication, blank=True)

    @staticmethod
    def update_fossil_count():
        for site in Site.objects.all():
            site.fossil_count = site.fossil_usages()
            site.save()

    def fossil_usages(self):
        return Fossil.objects.filter(site=self).count()

    def context_usages(self):
        return Context.objects.filter(site=self).count()
    #
    # def total_usages(self):
    #     return self.fossil_usages() + self.context_usages()

    def longitude(self):
        """
        Return the longitude for the point in the WGS84 datum
        see PaleoCoreOccurrenceBaseClass.gcs_coordinates
        :return:
        """
        return self.gcs_coordinates(coordinate='lon')

    def latitude(self):
        """
        Return the latitude for the point in the WGS84 datum
        see PaleoCoreOccurrenceBaseClass.gcs_coordinates
        :return:
        """
        return self.gcs_coordinates(coordinate='lat')

    def __str__(self):
        unicode_string = '['+str(self.id)+']'
        if self.name:
            unicode_string = unicode_string+' '+self.name
        elif self.verbatim_collection_name:
            unicode_string = unicode_string+' '+self.verbatim_collection_name
        return unicode_string

    class Meta:
        ordering = ['name']


class ActiveSite(Site):
    class Meta:
        proxy = True


class Context(projects.models.PaleoCoreContextBaseClass):
    """
    Inherits the following fields
    name, geological_formation, geological_member, geological_bed, older_interval, younger_interval,
    max_age, min_age, best_age
    """

    # Filter fields
    origins = models.BooleanField(default=False)

    # foreign keys
    reference = models.ForeignKey(to=Reference, on_delete=models.CASCADE, null=True, blank=True)
    # References
    references = models.ManyToManyField(publications.models.Publication, blank=True)
    site = models.ForeignKey(to=Site, on_delete=models.CASCADE, null=True, blank=True)

    # Original Fields from Paleobiology DB
    source = models.CharField(max_length=20, null=True, blank=True)
    verbatim_collection_no = models.IntegerField(blank=True, null=True)
    verbatim_record_type = models.CharField(max_length=20, null=True, blank=True)
    verbatim_formation = models.CharField(max_length=50, null=True, blank=True)
    verbatim_member = models.CharField(max_length=50, null=True, blank=True)
    verbatim_lng = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    verbatim_lat = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    verbatim_collection_name = models.CharField(max_length=200, null=True, blank=True)
    verbatim_collection_subset = models.CharField(max_length=20, null=True, blank=True)
    verbatim_collection_aka = models.CharField(max_length=200, null=True, blank=True)
    verbatim_n_occs = models.IntegerField(null=True, blank=True)

    verbatim_early_interval = models.CharField(max_length=50, null=True, blank=True)
    verbatim_late_interval = models.CharField(max_length=50, null=True, blank=True)
    verbatim_max_ma = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    verbatim_min_ma = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    verbatim_reference_no = models.IntegerField(null=True, blank=True)

    def has_ref(self):
        has_ref = False
        if self.reference:
            has_ref = True
        return has_ref

    # def latitude(self):S
    #     return self.gcs_coordinates('lat')
    #
    # def longitude(self):
    #     return self.gcs_coordinates('lon')

    class Meta:
        ordering = ['name']


class Fossil(models.Model):
    # Foreign keys
    context = models.ForeignKey(to=Context, on_delete=models.CASCADE, null=True, blank=True)

    # Fossil(Find)
    guid = models.URLField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    catalog_number = models.CharField(max_length=40, null=True, blank=True)
    other_catalog_numbers = models.CharField(max_length=255, null=True, blank=True)
    year_collected = models.IntegerField("Year", blank=True, null=True,
                                         help_text='The year, event or field campaign during which the item was found.')
    organism_id = models.CharField(max_length=40, null=True, blank=True)
    nickname = models.CharField(max_length=40, null=True, blank=True)
    holotype = models.BooleanField(default=False)
    lifestage = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    # Taxon
    taxon = models.ForeignKey(Taxon, null=True, blank=True, on_delete=models.SET_NULL)
    ttaxon = models.ForeignKey(TTaxon, null=True, blank=True, on_delete=models.SET_NULL)

    # Project
    project_name = models.CharField(max_length=100, null=True, blank=True)
    project_abbreviation = models.CharField(max_length=10, null=True, blank=True)
    collection_code = models.CharField(max_length=10, null=True, blank=True)

    # Location
    place_name = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=40, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
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
        return str(self.id)+' '+str(self.catalog_number)

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


class Photo(models.Model):
    image = models.ImageField('Image', upload_to='uploads/images/origins', null=True, blank=True)
    fossil = models.ForeignKey(Fossil, on_delete=models.CASCADE, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    default_image = models.BooleanField(default=False)

    def thumbnail(self):
        if self.image:  # test that the photo has an image.
            image_url = os.path.join(self.image.url)
            return mark_safe('<a href="{}"><img src="{}" style="width:300px" /></a>'.format(image_url, image_url))
        else:
            return None

    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True
    thumbnail.mark_safe = True

    class Meta:
        managed = True
        verbose_name = "Image"
        verbose_name_plural = "Images"


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name
