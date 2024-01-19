from hrp.models import TaxonRank, Biology
from rest_framework import serializers


class TaxonRankSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxonRank
        fields = ['name', 'plural', 'ordinal']


class BiologySerializer(serializers.ModelSerializer):
    """
    JSON serializer for the Biology class in hrp.models.taxon.py.
    This class controls what data are exposed through the API endpoint at
    https://paleocore.org/hrp/api/biology
    """

    class Meta:
        model = Biology
        # The fields listed here include ...
        fields = ['id',
                  'cat_number',
                  'basis_of_record',
                  'item_type',
                  'item_scientific_name',
                  'item_description',
                  'item_count',
                  'stratigraphic_formation',
                  'stratigraphic_member',
                  'collection_code',
                  'size_class',
                  'locality',
                  'longitude',
                  'latitude',
                  ]


