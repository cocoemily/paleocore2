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
    rank = serializers.StringRelatedField()
    name_reference = serializers.StringRelatedField()
    type_specimen = serializers.StringRelatedField()

    class Meta:
        model = Nomen
        fields = ['name', 'authorship', 'year', 'rank',
                  'type_specimen_label', 'type_specimen', 'paratypes',
                  'is_available', 'nomenclatural_status',
                  'is_objective_synonym', 'is_subjective_synonym',
                  'name_reference',
                  'verified_date', 'date_last_modified', 'full_name_html'
                  ]



