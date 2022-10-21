from django.db import models
from django.contrib.gis.db import models
import projects.models


class Person(projects.models.PaleoCoreBaseClass):
    family_name = models.CharField(max_length=255, blank=True, null=True)
    given_name = models.CharField(max_length=255, blank=True, null=True)


# Location - Locality design pattern
class Locality(projects.models.PaleoCoreLocalityBaseClass):
    """
    Locality Class <- PaleoCoreLocalityBaseClass <- PaleoCoreGeomBaseClass
    """
    locality_id = models.CharField(max_length=255, blank=True, null=True)
    collection_code = models.CharField(max_length=10, null=True, blank=True)
    #name: inheritied from base class
    formation = models.CharField(max_length=255, blank=True, null=True)
    member = models.CharField(max_length=255, blank=True, null=True)
    bed = models.TextField(null=True, blank=True)
    verbatim_age_ma = models.CharField(max_length=255, blank=True, null=True)
    earliest_age_ma = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    latest_age_ma = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    age_protocol = models.CharField(max_length=255, blank=True, null=True)
    year_established = models.IntegerField(null=True, blank=True)
    dimension_ew = models.CharField(max_length=255, blank=True, null=True)
    dimension_ns = models.CharField(max_length=255, blank=True, null=True)
    locality_description = models.TextField(null=True, blank=True)
    locality_boundary_east = models.CharField(max_length=255, blank=True, null=True)
    locality_boundary_north = models.CharField(max_length=255, blank=True, null=True)
    locality_boundary_south = models.CharField(max_length=255, blank=True, null=True)
    locality_boundary_west = models.CharField(max_length=255, blank=True, null=True)
    macrobotanical_evidence = models.CharField(max_length=255, blank=True, null=True)
    archaeological_evidence = models.CharField(max_length=255, blank=True, null=True)
    uncollected_taxa = models.CharField(max_length=255, blank=True, null=True)
    archaeology_present = models.BooleanField(null=True, blank=True)
    macrobotanical_present = models.BooleanField(null=True, blank=True)
    uncollected_fossils_present = models.BooleanField(null=True, blank=True)
    elevation = models.IntegerField(null=True, blank=True)
    georeference_protocol = models.CharField(max_length=255, blank=True, null=True)
    verbatim_row_data = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Locality'
        verbose_name_plural = 'Localities'
        ordering = ['locality_id']

    def __str__(self):
        return f"[{self.id}] {self.locality_id}"


class Specimen(projects.models.PaleoCoreOccurrenceBaseClass):
    """
    Specimen <- PaleoCoreOccurrenceBaseClass <- PaleoCoreGeomBaseClass <- PaleoCoreBaseClass
    """
    specimen_id = models.IntegerField(blank=True, null=True)
    collection_code = models.CharField("Collection Code", max_length=20, blank=True, null=True)
    item_number = models.IntegerField("Item #", null=True, blank=True)
    item_part = models.CharField("Item Part", max_length=10, null=True, blank=True)
    catalog_number = models.CharField("Catalog #", max_length=255, blank=True, null=True)
    scientific_name = models.CharField("Sci Name", max_length=255, null=True, blank=True)
    description = models.TextField("Description", blank=True, null=True)
    recorded_by = models.ForeignKey(Person, null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='recorded_specimens')
    # collector = models.CharField(max_length=50, blank=True, null=True)
    found_by = models.ForeignKey(Person, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='found_specimens')
    # found_by = models.CharField(max_length=50, blank=True, null=True)
    disposition = models.CharField(max_length=255, blank=True, null=True)
    preparations = models.CharField(max_length=50, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    formation = models.CharField(max_length=255, blank=True, null=True)
    member = models.CharField(max_length=255, blank=True, null=True)
    bed = models.TextField(blank=True, null=True)

    in_situ = models.BooleanField(null=True, blank=True)
    matrix_adhering = models.BooleanField(null=True, blank=True)

    locality = models.ForeignKey(Locality, null=True, blank=True, on_delete=models.SET_NULL)
    verbatim_row_data = models.TextField(null=True, blank=True)


class Fossil(Specimen):
    """
    A fossil specimen
    """
    organism_id = models.CharField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=50, blank=True, null=True)
    life_stage = models.CharField(max_length=50, blank=True, null=True)
    biology_remarks = models.TextField(max_length=500, null=True, blank=True)
    taxonomic_problem = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['catalog_number']

