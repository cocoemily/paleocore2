from django.contrib.gis.db import models
import projects.models
import publications.models
#from origins.models import Fossil, Reference
import origins.models


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
        return origins.models.Fossil.objects.filter(site=self).count()

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
    reference = models.ForeignKey(to='Reference', on_delete=models.CASCADE, null=True, blank=True)
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
