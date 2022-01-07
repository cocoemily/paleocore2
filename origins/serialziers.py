from origins.models import Nomen, TaxonRank
from rest_framework import serializers


class TaxonRankSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxonRank
        fields = ['name', 'plural', 'ordinal']


class NomenSerializer(serializers.ModelSerializer):
    # rank = serializers.HyperlinkedRelatedField(
    #     view_name='taxonrank',
    #     lookup_field='pk',
    #     read_only=True
    # )
    # taxon_rank_obj = serializers.StringRelatedField()
    # authorship_reference_obj = serializers.StringRelatedField()
    type_specimen = serializers.StringRelatedField()
    taxon_rank = serializers.CharField(source='taxon_rank_label')

    class Meta:
        model = Nomen
        fields = ['scientific_name', 'name', 'generic_name', 'specific_epithet',
                  'authorship', 'authorship_year', 'authorship_reference_id', 'scientific_name_id',
                  'taxon_rank', 'taxon_rank_group', 'nomenclatural_code', 'nomenclatural_status',
                  'type_specimen', 'paratypes', 'type_taxon', 'type_status',
                  'is_available',
                  'verified_date', 'date_last_modified'
                  ]



