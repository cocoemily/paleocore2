from django.conf.urls import url
from django.urls import include, path, re_path
from origins.models import Site, WorldBorder
from . import views
from rest_framework import routers


# REST framework routers
router = routers.DefaultRouter()
router.register(r'nomina', views.NomenViewSet)  # /paleocore.org/origins/api/nomina/
router.register(r'taxonranks', views.TaxonRankViewSet)

urlpatterns = [
    # url to get a geojson representation of all Origins sites
    # ex. /origins/origins.geojson  Note no trailing slash!

    # Uncomment to share origins geospatial data
    re_path(r'^origins.geojson$',
            views.MyGeoJSONLayerView.as_view(model=Site,
                                             crs=False,
                                             properties=['name', 'min_ma', 'max_ma', 'formation'],
                                             geometry_field='geom'),
            name='sites_geojson'),

    # Uncomment to expose countries geospatial dataset
    re_path(r'^countries.geojson$',
            views.MyGeoJSONLayerView.as_view(model=WorldBorder,
                                             crs=False,
                                             properties=['name', 'area', 'pop2005', 'fips'],
                                             geometry_field='mpoly'),
            name='countries_geojson'),

    #path('', views.index, name='index'),
    path('api/', include(router.urls)),  # wire in api paths
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('taxon/', views.TaxonListView.as_view(), name='taxon_list_view'),
    path('taxon/<int:pk>/', views.TaxonDetailView.as_view(), name='taxon_detail_view'),
    path('nomina/report/', views.NominaReportView.as_view(), name='nomina_report_view'),
    path('nomina/references/', views.NominaReferencesView.as_view(), name='nomina_references_view'),
    # path('/nomina/<int:pk>/', views.NomenDetailView.as_view(), name='nomen_detail_view'),
    # path('nomina/', views.NominaListView.as_view(), name='nomina_list_view'),
    # path('zotero/', views.ZoteroListView.as_view(), name='zotero_list_view')
]
