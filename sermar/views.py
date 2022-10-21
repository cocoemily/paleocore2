from django.shortcuts import render
from sermar.models import Locality, Collection, Occurrence
from rest_framework import viewsets
from rest_framework import permissions
from sermar.serializers import LocalitySerializer, CollectionSerializer, SpecimenSerializer
from djgeojson.views import GeoJSONLayerView
from djgeojson.serializers import Serializer as GeoJSONSerializer


# API Views
class LocalityGeoJSONView(GeoJSONLayerView):

    crs = False

    def render_to_response(self, context, **response_kwargs):
        serializer = GeoJSONSerializer()
        response = self.response_class(**response_kwargs)
        queryset = self.get_queryset()

        options = dict(properties=self.properties,
                       precision=self.precision,
                       simplify=self.simplify,
                       srid=self.srid,
                       geometry_field=self.geometry_field,
                       force2d=self.force2d,
                       bbox=self.bbox,
                       bbox_auto=self.bbox_auto,
                       use_natural_keys=self.use_natural_keys)
        serializer.serialize(queryset, stream=response, ensure_ascii=False,
                             crs=self.crs,  # in geoJSON crs is deprecated, raises error 36 in ol.source
                             **options)
        return response


class LocalityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Nomina to be viewed
    """
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer
    permission_classes = [permissions.IsAuthenticated]


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Taxon Ranks to be viewed
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

