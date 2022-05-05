from django.shortcuts import render
from sermar.models import Locality, Collection, Occurrence
from rest_framework import viewsets
from rest_framework import permissions
from sermar.serializers import LocalitySerializer, CollectionSerializer, SpecimenSerializer


# API Views
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

