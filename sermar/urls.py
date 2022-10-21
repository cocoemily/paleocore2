from django.conf.urls import url
from django.urls import include, path, re_path
from . import views
from .models import Locality
from .serializers import LocalitySerializer
from rest_framework import routers


# REST framework routers
router = routers.DefaultRouter()
router.register(r'localities', views.LocalityViewSet)  # /paleocore.org/sermar/api/localities/
#router.register(r'taxonranks', views.TaxonRankViewSet)

urlpatterns = [
    re_path(r'api/localities/geojson$',
            views.LocalityGeoJSONView.as_view(model=Locality,
                                              crs=False,
                                              properties=LocalitySerializer.Meta.fields,
                                              geometry_field='geom'),
            name='localities_geojson'),
    path('api/', include(router.urls)),  # wire in api paths
]
