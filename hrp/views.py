from django.shortcuts import render
from .serialziers import BiologySerializer, TaxonRankSerializer
from .models import Biology, TaxonRank
from rest_framework import viewsets
from rest_framework import permissions


# API Viewsets
class BiologyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Turkana Fossils to be viewed
    """

    queryset = Biology.objects.all()
    serializer_class = BiologySerializer
    permission_classes = [permissions.IsAuthenticated]


class TaxonRankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Taxon Ranks to be viewed
    """
    queryset = TaxonRank.objects.all()
    serializer_class = TaxonRankSerializer
    # permission_classes = [permissions.IsAuthenticated]
