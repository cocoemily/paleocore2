from django.contrib.gis.db import models


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
