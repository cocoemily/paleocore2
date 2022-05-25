from django.contrib.gis.db import models
import projects.models


class Person(projects.models.PaleoCoreBaseClass):
    family_name = models.CharField(max_length=255, blank=True, null=True)
    given_name = models.CharField(max_length=255, blank=True, null=True)


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
    verbatim_row_data = models.TextField(null=True, blank=True)
