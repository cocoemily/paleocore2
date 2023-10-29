from django.db import models
from projects.models import PaleoCoreBaseClass, PaleoCoreGeomBaseClass
from projects.models import PaleoCoreLocalityBaseClass, PaleoCoreOccurrenceBaseClass
from ckeditor.fields import RichTextField
from projects import ontologies as projects_ontologies
from .otnologies import ACCUMULATOR_CHOICES, PARK_CHOICES
from django.utils.html import mark_safe
import os

# Choices
tyto_alba = 'Tyto alba'
bubo_africanus = 'Bubo africanus'
bubo_lacteus = 'Bubo lacteus'
OWL_CHOICES = (
    (tyto_alba, 'Tyto alba'),
    (bubo_africanus, 'Bubo africanus'),
    (bubo_lacteus, 'Bubo lacteus')
)

# Map shapefile fields to model for import with LayerMapping
mapping = {
    'roost_id': 'ROOSTS_ID',
    'priority': 'PRIORITY',
    'verbatim_in_park': 'INPARK',
    'owls': 'OWLS',
    'owl_species': 'OWL_SP',
    'verbatim_pellets': 'PELLETS',
    'pellet_species': 'PELLET_SP',
    'verbatim_bones': 'BONES',
    'sample_size': 'SMPL_SIZE',
    'landmark': 'KOP_LANDM',
    'verbatim_easting': 'UTM_EAST',
    'verbatim_northing': 'UTM_NORTH',
    'verbatim_utm_zone': 'UTM_ZONE',
    'verbatim_roost_type': 'ROOST_TYPE',
    'adequate_sample': 'ADEQ_SMPL',
    'verbatim_analysis': 'Analysis',
    'geom': 'POINT'
}


class Locality(PaleoCoreGeomBaseClass):
    """
    Class for roost/nest localities
    inherits from PaleoCoreGeomBaseClass
    name
    date_created, date_last_modified
    problem, problem_comment
    remarks, last_import

    georeference_remarks
    geom
    objects
    gcs_coordinates(), utm_coordinates(), point_x(), point_y()
    longitude(), latitude(), easting(), northing()
    """
    roost_id = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    verbatim_in_park = models.IntegerField(null=True, blank=True)
    in_park = models.BooleanField(null=True)
    owls = models.IntegerField(null=True, blank=True)
    owl_species = models.CharField(max_length=256, null=True, blank=True, choices=OWL_CHOICES)
    verbatim_pellets = models.IntegerField(null=True, blank=True)
    pellets = models.BooleanField(null=True, blank=True)
    pellet_species = models.CharField(max_length=256, null=True, blank=True, choices=OWL_CHOICES)
    verbatim_bones = models.IntegerField(null=True, blank=True)
    bones = models.BooleanField(null=True)
    sample_size = models.IntegerField(null=True, blank=True)
    landmark = models.CharField(null=True, blank=True, max_length=256)
    verbatim_easting = models.IntegerField(null=True, blank=True)
    verbatim_northing = models.IntegerField(null=True, blank=True)
    verbatim_utm_zone = models.IntegerField(null=True, blank=True)
    verbatim_roost_type = models.CharField(null=True, blank=True, max_length=256)
    roost_type = models.CharField(null=True, blank=True, max_length=256)
    adequate_sample = models.BooleanField(null=True)
    verbatim_analysis = models.IntegerField(null=True, blank=True)
    analysis = models.BooleanField(null=True)
    accumulating_agent = models.CharField(max_length=255, null=True, blank=True, choices=ACCUMULATOR_CHOICES)
    protected_area = models.CharField(max_length=255, null=True, blank=True, choices=PARK_CHOICES)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Locality"
        verbose_name_plural = "Localities"


class Collection(PaleoCoreBaseClass):
    """
    Class for collections made at localities. Many locations at each locality
    inherits from PaleoCoreBaseClass
    name
    date_created, date_last_modified
    problem, problem_comment
    remarks, last_import
    """
    collection_code = models.IntegerField(null=True, blank=True)
    roost_id = models.IntegerField(null=True, blank=True)
    locality = models.ForeignKey(Locality, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.IntegerField(null=True, blank=True)
    date = models.DateField('Date Collected', null=True, blank=True)
    specimen_loc = models.CharField(max_length=256, null=True, blank=True)
    disposition = models.CharField(max_length=256, null=True, blank=True)
    spec_start = models.IntegerField(null=True, blank=True)
    spec_end = models.IntegerField(null=True, blank=True)
    sample_size = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    comments = RichTextField(null=True, blank=True)
    bags = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    accumulating_agent = models.CharField(max_length=255, null=True, blank=True, choices=ACCUMULATOR_CHOICES)

    def __str__(self):
        # return f'{self.collection_code}'
        return self.label()

    def label(self):
        # return f'C{self.collection_code}_R{self.roost_id}_D{self.date.year}{self.date.month}{self.date.day}'
        return 'C{:3d}-R{}-D{}'.format(self.collection_code, self.roost_id, self.date.strftime("%Y%b%d"))


class Occurrence(PaleoCoreOccurrenceBaseClass):
    # date_last_modified = models.DateTimeField("Date Last Modified", auto_now=True)
    basis_of_record = models.CharField("Basis of Record", max_length=50, blank=True, null=False,
                                       choices=projects_ontologies.BASIS_OF_RECORD_VOCABULARY)  # NOT NULL Preserved Specimen
    item_type = models.CharField("Item Type", max_length=255, blank=True, null=False,
                                 choices=projects_ontologies.ITEM_TYPE_VOCABULARY)  # NOT NULL, Faunal
    collection_code = models.CharField("Collection Code", max_length=20, blank=True, null=True) # populated with numerical collection codes
    item_number = models.IntegerField("Item #", null=True, blank=True) # unique specimen number by collection
    item_part = models.CharField("Item Part", max_length=10, null=True, blank=True) # empty, delete field
    item_scientific_name = models.CharField("Sci Name", max_length=255, null=True, blank=True) # Scientific names
    item_description = models.CharField("Description", max_length=255, blank=True, null=True) # Anatomical description
    collecting_method = models.CharField("Collecting Method", max_length=50, # surface standard
                                         choices=projects_ontologies.COLLECTING_METHOD_VOCABULARY, null=False)
    related_catalog_items = models.CharField("Related Catalog Items", max_length=50, null=True, blank=True)
    collector = models.CharField(max_length=50, blank=True, null=True, default='Denné Reed') # Denne Reed
    finder = models.CharField(null=True, blank=True, max_length=50, default='Denné Reed') # Denne Reed
    loan = models.CharField(max_length=255, blank=True, null=True) # Scott Bluementhal
    loan_date = models.DateTimeField(blank=True, null=True) # date of loan
    disposition = models.CharField(max_length=255, blank=True, null=True) # current storage location
    field_number_orig = models.DateTimeField(blank=True, null=True, editable=True) # datetime of collection
    individual_count = models.IntegerField(blank=True, null=True, default=1) # number of individual represented by specimen
    preparation_status = models.CharField(max_length=50, blank=True, null=True) #
    in_situ = models.BooleanField(default=False)
    image = models.FileField(max_length=255, blank=True, upload_to="uploads/images/drp", null=True)
    weathering = models.SmallIntegerField(blank=True, null=True)
    surface_modification = models.CharField(max_length=255, blank=True, null=True)
    # locality = models.ForeignKey(Locality, null=True, blank=True, on_delete=models.SET_NULL)
    collection = models.ForeignKey(Collection, null=True, blank=True, on_delete=models.SET_NULL)


class Biology(Occurrence):
    infraspecific_epithet = models.CharField(null=True, blank=True, max_length=50)
    infraspecific_rank = models.CharField(null=True, blank=True, max_length=50)
    author_year_of_scientific_name = models.CharField(null=True, blank=True, max_length=50)
    nomenclatural_code = models.CharField(null=True, blank=True, max_length=50)
    # identification_qualifier = models.CharField(null=True, blank=True, max_length=50)
    identified_by = models.CharField(null=True, blank=True, max_length=100)
    date_identified = models.DateTimeField(null=True, blank=True)
    type_status = models.CharField(null=True, blank=True, max_length=50)
    sex = models.CharField(null=True, blank=True, max_length=50)
    life_stage = models.CharField(null=True, blank=True, max_length=50)
    preparations = models.CharField(null=True, blank=True, max_length=50)
    morphobank_number = models.IntegerField(null=True, blank=True)
    side = models.CharField(null=True, blank=True, max_length=50)
    attributes = models.CharField(null=True, blank=True, max_length=50)
    fauna_notes = models.TextField(null=True, blank=True, max_length=64000)
    tooth_upper_or_lower = models.CharField(null=True, blank=True, max_length=50)
    tooth_number = models.CharField(null=True, blank=True, max_length=50)
    tooth_type = models.CharField(null=True, blank=True, max_length=50)
    um_tooth_row_length_mm = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    um_1_length_mm = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    um_1_width_mm = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    um_2_length_mm = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    um_2_width_mm = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    um_3_length_mm = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    um_3_width_mm = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    lm_tooth_row_length_mm = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    lm_1_length = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    lm_1_width = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    lm_2_length = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    lm_2_width = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    lm_3_length = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    lm_3_width = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    element_id = models.IntegerField(null=True, blank=True)
    element = models.CharField(null=True, blank=True, max_length=50)
    element_modifier = models.CharField(null=True, blank=True, max_length=50)
    uli1 = models.BooleanField(default=False)
    uli2 = models.BooleanField(default=False)
    uli3 = models.BooleanField(default=False)
    uli4 = models.BooleanField(default=False)
    uli5 = models.BooleanField(default=False)
    uri1 = models.BooleanField(default=False)
    uri2 = models.BooleanField(default=False)
    uri3 = models.BooleanField(default=False)
    uri4 = models.BooleanField(default=False)
    uri5 = models.BooleanField(default=False)
    ulc = models.BooleanField(default=False)
    urc = models.BooleanField(default=False)
    ulp1 = models.BooleanField(default=False)
    ulp2 = models.BooleanField(default=False)
    ulp3 = models.BooleanField(default=False)
    ulp4 = models.BooleanField(default=False)
    urp1 = models.BooleanField(default=False)
    urp2 = models.BooleanField(default=False)
    urp3 = models.BooleanField(default=False)
    urp4 = models.BooleanField(default=False)
    ulm1 = models.BooleanField(default=False)
    ulm2 = models.BooleanField(default=False)
    ulm3 = models.BooleanField(default=False)
    urm1 = models.BooleanField(default=False)
    urm2 = models.BooleanField(default=False)
    urm3 = models.BooleanField(default=False)
    lli1 = models.BooleanField(default=False)
    lli2 = models.BooleanField(default=False)
    lli3 = models.BooleanField(default=False)
    lli4 = models.BooleanField(default=False)
    lli5 = models.BooleanField(default=False)
    lri1 = models.BooleanField(default=False)
    lri2 = models.BooleanField(default=False)
    lri3 = models.BooleanField(default=False)
    lri4 = models.BooleanField(default=False)
    lri5 = models.BooleanField(default=False)
    llc = models.BooleanField(default=False)
    lrc = models.BooleanField(default=False)
    llp1 = models.BooleanField(default=False)
    llp2 = models.BooleanField(default=False)
    llp3 = models.BooleanField(default=False)
    llp4 = models.BooleanField(default=False)
    lrp1 = models.BooleanField(default=False)
    lrp2 = models.BooleanField(default=False)
    lrp3 = models.BooleanField(default=False)
    lrp4 = models.BooleanField(default=False)
    llm1 = models.BooleanField(default=False)
    llm2 = models.BooleanField(default=False)
    llm3 = models.BooleanField(default=False)
    lrm1 = models.BooleanField(default=False)
    lrm2 = models.BooleanField(default=False)
    lrm3 = models.BooleanField(default=False)
    verbatim_morphotype_id = models.IntegerField(null=True, blank=True)
    morphotype = models.ForeignKey('Morphotype', null=True, blank=True, on_delete=models.SET_NULL)
    # taxon = models.ForeignKey(Taxon,
    #                           default=0, on_delete=models.SET_DEFAULT,  # prevent deletion when taxa deleted
    #                           related_name='drp_biology_occurrences')
    # identification_qualifier = models.ForeignKey(IdentificationQualifier, null=True, blank=True,
    #                                              on_delete=models.SET_NULL,
    #                                              related_name='drp_biology_occurrences')

    class Meta:
        verbose_name = "Biology Occurrence"
        verbose_name_plural = "Biology Occurrences"

    def __str__(self):
        return str(self.catalog_number)

    def default_image(self):
        """
        Function to fetch a default thumbnail image for a fossil
        :return:
        """
        images = self.specimenphoto_set.filter(default_image=True)
        if images.count() >= 1:
            return images[0].thumbnail()
        else:
            return None
class Morphotype(PaleoCoreBaseClass):
    """
    Class model for morphotypes. Many biology occurrences for each morphotype
    inherits from PaleoCoreBaseClass
    name
    date_created, date_last_modified
    problem, problem_comment
    remarks, last_import
    """
    # name is used for morph_name
    # remarks is used for comments
    morph_id = models.IntegerField(null=True, blank=True)
    order_id = models.IntegerField(null=True, blank=True)
    species1_id = models.IntegerField(null=True, blank=True)
    species2_id = models.IntegerField(null=True, blank=True)
    species3_id = models.IntegerField(null=True, blank=True)
    species4_id = models.IntegerField(null=True, blank=True)
    analysis_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'[{self.morph_id}]{self.name}'


class SpecimenPhoto(models.Model):
    image = models.ImageField('Image', upload_to='uploads/images/sermar', null=True, blank=True)
    occurrence = models.ForeignKey('Occurrence', on_delete=models.CASCADE, null=True, blank=False)
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
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
