from django.contrib import admin
from .models import Specimen


# Register your models here.
class SpecimenAdmin(admin.ModelAdmin):
    list_display = ['id', 'catalog_number', 'verbatim_row_data']


admin.site.register(Specimen, SpecimenAdmin)
