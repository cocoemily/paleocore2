from django.conf.urls import url
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    # e.g. /paleosites/
    path('', views.home, name='home'),
    # e.g. /paleosites/index/
    path('index', views.home, name='home'),
    # e.g. /paleosites/kml/
    path('kml/', views.all_kml, name='all_kml'),
    # e.g. /paleosites/map/
    path('map/', views.map_page, name='map_page'),
]
