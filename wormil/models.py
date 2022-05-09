from django.db import models
from django.contrib.gis.db import models
import projects.models


class Locality(projects.models.PaleoCoreLocalityBaseClass):

    class Meta:
        verbose_name = 'Locality'
        verbose_name_plural = 'Localities'


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
    description = models.CharField("Description", max_length=255, blank=True, null=True)
    collector = models.CharField(max_length=50, blank=True, null=True)
    finder = models.CharField(max_length=50, blank=True, null=True)
    disposition = models.CharField(max_length=255, blank=True, null=True)
    preparations = models.CharField(max_length=50, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    formation = models.CharField(max_length=255, blank=True, null=True)
    member = models.CharField(max_length=255, blank=True, null=True)
    bed = models.CharField(max_length=255, blank=True, null=True)

    in_situ = models.BooleanField(null=True, blank=True)
    matrix_adhering = models.BooleanField(null=True, blank=True)

    locality = models.ForeignKey(Locality, null=True, blank=True, on_delete=models.SET_NULL)
    verbatim_row_data = models.TextField(null=True, blank=True)


class Fossil(Specimen):
    """
    A fossil specimen
    """
    sex = models.CharField(max_length=50, blank=True, null=True)
    life_stage = models.CharField(max_length=50, blank=True, null=True)
    biology_remarks = models.TextField(max_length=500, null=True, blank=True)

