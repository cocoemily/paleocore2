from django.contrib import admin
from .models import Fossil, Locality
from projects.admin import PaleoCoreLocalityAdminGoogle, PaleoCoreOccurrenceAdmin


# Register your models here.
class FossilAdmin(PaleoCoreOccurrenceAdmin):
    list_display = ['id', 'catalog_number', 'description', 'latitude', 'longitude']
    readonly_fields = ['latitude', 'longitude']


admin.site.register(Fossil, FossilAdmin)
admin.site.register(Locality, PaleoCoreLocalityAdminGoogle)
