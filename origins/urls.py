from django.conf.urls import url
from origins.models import Site, WorldBorder
from .views import MyGeoJSONLayerView

urlpatterns = [
    # url to get a geojson representation of all Origins sites
    # ex. /origins/origins.geojson  Note no trailing slash!
    url(r'^origins.geojson$',
        MyGeoJSONLayerView.as_view(model=Site,
                                   crs=False,
                                   properties=['name', 'min_ma', 'max_ma', 'formation'],
                                   geometry_field='geom'),
        name='sites_geojson'),
url(r'^countries.geojson$',
        MyGeoJSONLayerView.as_view(model=WorldBorder,
                                   crs=False,
                                   properties=['name', 'area', 'pop2005', 'fips'],
                                   geometry_field='mpoly'),
        name='countries_geojson'),
]
