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

    class Meta:
        model = Nomen
        fields = ['name', 'authorship', 'year', 'rank']



