from django.urls import include, path
from hrp import views as hrp_views
from django.contrib.auth.decorators import login_required
from rest_framework import routers

# REST framework routers
router = routers.DefaultRouter()
router.register(r'biology', hrp_views.BiologyViewSet)  # /paleocore.org/projects/hrp/api/biology/
router.register(r'taxonranks', hrp_views.TaxonRankViewSet)  # /paleocore.org/projects/hrp/api/taxonranks/


urlpatterns = [
    # Project URLs are included by main urls.py
    path('api/', include(router.urls)),  # wire in api paths
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # /projects/hrp/upload/
    # path('upload/', login_required(hrp_views.UploadKMLView.as_view(), login_url='/login/'), name="hrp_upload_kml"),

    # /projects/hrp/download/
    # url(r'^download/$', hrp_views.DownloadKMLView.as_view(), name="hrp_download_kml"),

    # /projects/hrp/confirmation/
    # url(r'^confirmation/$', hrp_views.Confirmation.as_view(), name="hrp_upload_confirmation"),

    # /projects/hrp/upload/shapefile/
    # url(r'^upload/shapefile/', hrp_views.UploadShapefileView.as_view(), name="hrp_upload_shapefile"),

    # /projects/hrp/change_xy/
    # url(r'^change_xy/', hrp_views.change_coordinates_view, name="hrp_change_xy"),
]
