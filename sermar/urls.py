from django.conf.urls import url
from django.urls import include, path, re_path
from . import views
from rest_framework import routers


# REST framework routers
router = routers.DefaultRouter()
router.register(r'localities', views.LocalityViewSet)  # /paleocore.org/sermar/api/localities/
#router.register(r'taxonranks', views.TaxonRankViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # wire in api paths
]
