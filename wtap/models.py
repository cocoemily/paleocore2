from django.contrib.gis.db import models
import projects.models
from .ontologies import BASIS_OF_RECORD_VOCABULARY, ITEM_TYPE_VOCABULARY, COLLECTING_METHOD_VOCABULARY, \
    COLLECTOR_CHOICES, FIELD_SEASON_CHOICES, SIDE_VOCABULARY

# Constants
app_name = 'wtap'


# Models
class Occurrence(projects.models.PaleoCoreOccurrenceBaseClass):
    """
    Occurrence <- PaleoCoreOccurrenceBaseClass <- PaleoCoreGeomBaseClass <- PaleoCoreBaseClass
    """
    basis_of_record = models.CharField("Basis of Record", max_length=50, blank=True, null=False,
                                       choices=BASIS_OF_RECORD_VOCABULARY)  # NOT NULL
    item_type = models.CharField("Item Type", max_length=255, blank=True, null=False,
                                 choices=ITEM_TYPE_VOCABULARY)  # NOT NULL
    collection_code = models.CharField("Collection Code", max_length=20, blank=True, null=True, default='WT')
    # Note we're not using localities!
    item_number = models.IntegerField("Item #", null=True, blank=True)
    item_part = models.CharField("Item Part", max_length=10, null=True, blank=True)
    catalog_number = models.CharField("Catalog #", max_length=255, blank=True, null=True)
    item_scientific_name = models.CharField("Sci Name", max_length=255, null=True, blank=True)
    item_description = models.CharField("Description", max_length=255, blank=True, null=True)
    # georeference_remarks = models.CharField(max_length=50, null=True, blank=True)
    collecting_method = models.CharField("Collecting Method", max_length=50,
                                         choices=COLLECTING_METHOD_VOCABULARY, null=False)  # NOT NULL
    related_catalog_items = models.CharField("Related Catalog Items", max_length=50, null=True, blank=True)
    collector = models.CharField(max_length=50, blank=True, null=True, choices=COLLECTOR_CHOICES)
    finder = models.CharField(max_length=50, blank=True, null=True)
    disposition = models.CharField(max_length=255, blank=True, null=True)
    field_season = models.CharField(max_length=50, null=True, blank=True, choices=FIELD_SEASON_CHOICES)
    individual_count = models.IntegerField(blank=True, null=True, default=1)
    preparation_status = models.CharField(max_length=50, blank=True, null=True)
    stratigraphic_marker_upper = models.CharField(max_length=255, blank=True, null=True)
    distance_from_upper = models.DecimalField(max_digits=38, decimal_places=8, blank=True, null=True)
    stratigraphic_marker_lower = models.CharField(max_length=255, blank=True, null=True)
    distance_from_lower = models.DecimalField(max_digits=38, decimal_places=8, blank=True, null=True)
    stratigraphic_marker_found = models.CharField(max_length=255, blank=True, null=True)
    distance_from_found = models.DecimalField(max_digits=38, decimal_places=8, blank=True, null=True)
    stratigraphic_marker_likely = models.CharField(max_length=255, blank=True, null=True)
    distance_from_likely = models.DecimalField(max_digits=38, decimal_places=8, blank=True, null=True)
    stratigraphic_member = models.CharField(max_length=255, blank=True, null=True)
    analytical_unit = models.CharField("Submember", max_length=255, blank=True, null=True)
    analytical_unit_2 = models.CharField(max_length=255, blank=True, null=True)
    analytical_unit_3 = models.CharField(max_length=255, blank=True, null=True)
    in_situ = models.BooleanField(default=False)
    ranked = models.BooleanField(default=False)
    image = models.FileField(max_length=255, blank=True, upload_to="uploads/images/mlp", null=True)
    weathering = models.SmallIntegerField(blank=True, null=True)
    surface_modification = models.CharField(max_length=255, blank=True, null=True)

    # Verbatim Fields
    verbatim_kml_data = models.TextField(null=True, blank=True)

    def __str__(self):
        """
        What is the best string representation for an occurrence instance?
        All collected items have catalogue numbers, but observations do not
        This method returns the catalog number if it exists, or a string with the id value
        if there is no catalog number.
        """
        if self.catalog_number:
            return self.catalog_number
        else:
            return "item "+str(self.id)

    class Meta:
        managed = True
        verbose_name = app_name.upper()+" Occurrence"
        verbose_name_plural = app_name.upper()+" Occurrences"


class Artifact(Occurrence):
    find_type = models.CharField(null=True, blank=True, max_length=255)
    length_mm = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    width_mm = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    # dataclass = models.CharField(max_length=20, blank=True, null=True)
    cortex = models.CharField(max_length=10, blank=True, null=True)
    technique = models.CharField(max_length=20, blank=True, null=True)
    alteration = models.CharField(max_length=20, blank=True, null=True)
    edge_damage = models.CharField(max_length=20, blank=True, null=True)
    fb_type = models.IntegerField('Bordes Type', blank=True, null=True)
    fb_type_2 = models.IntegerField('Bordes Type 2', blank=True, null=True)
    fb_type_3 = models.IntegerField('Bordes Type 3', blank=True, null=True)
    platform_surface = models.CharField(max_length=20, blank=True, null=True)
    platform_exterior = models.CharField(max_length=20, blank=True, null=True)
    form = models.CharField(max_length=20, blank=True, null=True)
    scar_morphology = models.CharField(max_length=20, blank=True, null=True)
    retouched_edges = models.IntegerField(blank=True, null=True)
    retouch_intensity = models.CharField(max_length=20, blank=True, null=True)
    reprise = models.CharField(max_length=20, blank=True, null=True)
    maximum_width = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    thickness = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    platform_width = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    platform_thickness = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    raw_material = models.CharField(max_length=20, blank=True, null=True)
    exterior_surface = models.CharField(max_length=20, blank=True, null=True)
    exterior_type = models.CharField(max_length=20, blank=True, null=True)
    weight = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    platform_technique = models.CharField(max_length=20, blank=True, null=True)
    platform_angle = models.DecimalField(decimal_places=0, max_digits=3, null=True, blank=True)
    multiple = models.BooleanField(default=False, blank=True, null=True)
    epa = models.IntegerField(blank=True, null=True)
    core_shape = models.CharField(max_length=20, blank=True, null=True)
    core_blank = models.CharField(max_length=20, blank=True, null=True)
    core_surface_percentage = models.DecimalField(decimal_places=0, max_digits=3, blank=True, null=True)
    proximal_removals = models.IntegerField(blank=True, null=True)
    prepared_platforms = models.IntegerField(blank=True, null=True)
    flake_direction = models.CharField(max_length=20, blank=True, null=True)
    scar_length = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    scar_width = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    artifact_remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = app_name.upper()+" Artifact"
        verbose_name_plural = app_name.upper()+" Artifacts"


class Fossil(Occurrence):
    """
    Biology <- Occurrence <- PaleoCoreOccurrenceBaseClass <- PaleoCoreGeomBaseClass <- PaleoCoreBaseClass
    """
    infraspecific_epithet = models.CharField(null=True, blank=True, max_length=50)
    infraspecific_rank = models.CharField(null=True, blank=True, max_length=50)
    author_year_of_scientific_name = models.CharField(null=True, blank=True, max_length=50)
    nomenclatural_code = models.CharField(null=True, blank=True, max_length=50)
    identified_by = models.CharField(null=True, blank=True, max_length=100, choices=COLLECTOR_CHOICES)
    date_identified = models.DateTimeField(null=True, blank=True)
    identification_remarks = models.TextField(null=True, blank=True, max_length=64000)
    type_status = models.CharField(null=True, blank=True, max_length=50)
    sex = models.CharField(null=True, blank=True, max_length=50)
    life_stage = models.CharField(null=True, blank=True, max_length=50)
    preparations = models.CharField(null=True, blank=True, max_length=50)
    morphobank_number = models.IntegerField(null=True, blank=True)
    side = models.CharField(null=True, blank=True, max_length=50, choices=SIDE_VOCABULARY)
    attributes = models.CharField(null=True, blank=True, max_length=50)
    tooth_upper_or_lower = models.CharField(null=True, blank=True, max_length=10)
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
    taxon = models.ForeignKey('Taxon',
                              default=0, on_delete=models.SET_DEFAULT,  # prevent deletion when taxa deleted
                              related_name='mlp_biology_occurrences')
    identification_qualifier = models.ForeignKey('IdentificationQualifier', null=True, blank=True,
                                                 on_delete=models.SET_NULL,
                                                 related_name='mlp_biology_occurrences')

    def __str__(self):
        return str(self.taxon.__str__())

    def match_taxon(self):
        """
        find taxon objects from item_scientific_name
        Return: (True/False, match_count, match_list)
        """
        match_list = Taxon.objects.filter(name=self.item_scientific_name)
        if len(match_list) == 1:  # one match
            result_tuple = (True, 1, match_list)
        else:
            result_tuple = (False, len(match_list), match_list)
        return result_tuple

    class Meta:
        verbose_name = app_name.upper()+" Fossil"
        verbose_name_plural = app_name.upper()+" Fossils"


class Rock(Occurrence):
    find_type = models.CharField(null=True, blank=True, max_length=255)
    dip = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    strike = models.DecimalField(max_digits=38, decimal_places=8, null=True, blank=True)
    color = models.CharField(null=True, blank=True, max_length=255)
    texture = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        verbose_name = app_name.upper()+" Rock"
        verbose_name_plural = app_name.upper()+" Rocks"


class TaxonRank(projects.models.TaxonRank):
    class Meta:
        verbose_name = app_name.upper()+" Taxon Rank"
        verbose_name_plural = app_name.upper()+" Taxon Ranks"


class Taxon(projects.models.Taxon):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    rank = models.ForeignKey('TaxonRank', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = app_name.upper()+" Taxon"
        verbose_name_plural = app_name.upper()+" Taxa"
        ordering = ['rank__ordinal', 'name']


class IdentificationQualifier(projects.models.IdentificationQualifier):

    class Meta:
        verbose_name = app_name.upper()+" ID Qualifier"
