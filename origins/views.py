from django.shortcuts import render
from django.views import generic
from .forms import UpdateSitesForm, UpdateSitesModelForm
from .models import Fossil, TTaxon, TaxonRank, Nomen
from django.contrib import messages
from djgeojson.views import GeoJSONLayerView, GeoJSONResponseMixin
from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from pyzotero import zotero

from rest_framework import viewsets
from rest_framework import permissions
from origins.serialziers import TaxonRankSerializer, NomenSerializer


class UpdateSites(generic.FormView):
    template_name = 'admin/origins/site/update_sites.html'
    form_class = UpdateSitesModelForm
    context_object_name = 'upload'
    success_url = '../'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        idstring = self.request.GET['ids']
        idlist = idstring.split(',')
        new_site = form.cleaned_data['site']
        update_count = 0
        for fossil_id in idlist:
            fossil = Fossil.objects.get(pk=fossil_id)
            fossil.site = new_site
            fossil.save()
            update_count += 1
        if update_count == 1:
            count_string = '1 record'
        if update_count > 1:
            count_string = '{} records'.format(update_count)
        messages.add_message(self.request, messages.INFO, 'Successfully updated {}'.format(count_string))
        return super(UpdateSites, self).form_valid(form)


class MyGeoJSONLayerView(GeoJSONLayerView):

    crs = False

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
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


def index(request):
    return HttpResponse("Hello, world. You're at the Origins index.")


class TaxonListView(generic.ListView):
    #template_name = 'taxalist.html'
    context_object_name = 'taxa'

    def get_queryset(self):
        """Return a list of taxa """
        # get just the non-class paleocore terms, which get added to the context as terms
        taxa = TTaxon.objects.filter(classification_status='accepted')
        return taxa

    # def get_context_data(self, **kwargs):
    #     # supplement the context by adding a list of class terms
    #
    #     # get the original context
    #     context = super(TaxaListView, self).get_context_data(**kwargs)
    #
    #     # get a queryset of just paleocore classes
    #     paleocore_classes = Term.objects.filter(projects__name='pc').filter(is_class=True).order_by('term_ordering')
    #
    #     # add them to the context, which now contains elements for terms and classes
    #     context['classes'] = paleocore_classes
    #     return context


class TaxonDetailView(generic.DetailView):
    model = TTaxon

# This view is replaced by NominaListView in models.wagtail
# class NominaListView(generic.ListView):
#     template_name = 'origins/nomina.html'
#     context_object_name = 'taxa'
#     model = TTaxon
#
#     def get_queryset(self):
#         """Return a list of all species names"""
#         species = TaxonRank.objects.get(name='Species')
#         taxa = TTaxon.objects.filter(rank=species).order_by('name')
#         return taxa


# class NomenDetailView(generic.DetailView):
#     model = Nomen
    #template_name = 'nomen_detail.html'


class ZoteroListView(generic.ListView):
    template_name = 'origins/zotero_list.html'
    context_object_name = 'zotero'

    def get_queryset(self):
        """Get a queryset from Zotero"""
        zot = zotero.Zotero(2207794, 'user', 'ZRvebf2xkInRdYxVGtALHvzZ')
        items = zot.top(limit=20)
        return items


# API Views
class NomenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Nomina to be viewed
    """
    queryset = Nomen.objects.all()
    serializer_class = NomenSerializer
    #permission_classes = [permissions.IsAuthenticated]


class TaxonRankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Taxon Ranks to be viewed
    """
    queryset = TaxonRank.objects.all()
    serializer_class = TaxonRankSerializer
    #permission_classes = [permissions.IsAuthenticated]

