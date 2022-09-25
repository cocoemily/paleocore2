from origins.models import Nomen, TaxonRank
from rest_framework import serializers


class TaxonRankSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxonRank
        fields = ['name', 'plural', 'ordinal']


class NomenSerializer(serializers.ModelSerializer):
    """
    JSON serializer for Nomen class in origins.models.taxon.py.
    This class controls whata data are exposed through the API endpoint at
    https://paleocore.org/origins/api/nomina
    """

    # Two fields need special treatment because they are foreign key fields. The two approaches essentially produce
    # the same result -- a string representation of the related object -- but with different methods.
    # For the type_specimen field we retrieve the string representation of the type specimen object using the
    # StringRelatedField class of the serializer library.
    # For the taxon_rank field we specify calling the taxon_rank_label method of the Nomen class
    # which gets a string representation of the taxon rank, but one that is slightly different than the standard
    # string representation generated by the __str__ method of the TaxonRank class.
    type_specimen = serializers.StringRelatedField()
    taxon_rank = serializers.CharField(source='taxon_rank_label')

    class Meta:
        model = Nomen
        # The fields listed here include all the documented fields of the Nomen class plus a few others.
        fields = ['scientific_name', 'name', 'generic_name', 'specific_epithet',
                  'authorship', 'authorship_year', 'authorship_reference', 'authorship_reference_id',
                  'scientific_name_id',
                  'taxon_rank', 'taxon_rank_group', 'nomenclatural_code', 'nomenclatural_status', 'status_remark',
                  'type_specimen', 'paratypes', 'type_taxon', 'type_status',
                  'is_available',
                  'verified_date', 'date_last_modified'
                  ]
