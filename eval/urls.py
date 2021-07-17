from django.conf.urls import url
from . import views

urlpatterns = [
# ex /eval/
    url(r'^$', views.ActiveStudentListView.as_view(), name='students'),
    # ex /meetings/2013/
    url(r'^(?P<pk>[0-9]+)/$', views.ActiveStudentDetailView.as_view(), name='student_detail'),
               # url to get a geojson representation of all Origins sites
               # ex. /origins/sites.geojson

]
