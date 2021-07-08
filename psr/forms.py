from django import forms
from psr.models import *


class UploadShapefile(forms.Form):
    shpfileUpload = forms.FileField(
        label='Upload a shape file, *.shp',
    )
    # shpIndexUpload = forms.FileField(
    #     label='Upload a shape file index, *.shx',
    # )
    shpfileDataUpload = forms.FileField(
        label='Upload shape file data, *.dbf',
    )

    photoUpload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label='Upload all photos',
    )


class UploadShapefileDirectory(forms.Form):
    shapefileUpload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}),
        label='Upload shapefile directory',
    )


class UploadMDB(forms.Form):
    mdbUpload = forms.FileField(
        label='Upload an Access Database, *.mdb',
        widget=forms.FileInput(attrs={'accept': 'application/mdb'}) #not actually a file type, so doesn't limit
    )


class UploadJSON(forms.Form):
    jsonUpload = forms.FileField(
        label='Upload a JSON file, *.json',
        widget=forms.FileInput(attrs={'accept':'application/json'})
    )



# class UploadKMLForm(forms.Form):
#     kmlfileUpload = forms.FileField(
#         label='Upload a kml/kmz file, *.kml or *.kmz ',
#     )
#
# class DeleteAllForm(forms.Form):
#     pass
#
# class DownloadKMLForm(forms.Form):
#     FILE_TYPE_CHOICES = (('1', 'KML',), ('2', 'KMZ',))
#     kmlfileDownload = forms.ChoiceField(
#         required=False,
#         widget=forms.RadioSelect,
#         choices=FILE_TYPE_CHOICES,
#         label="File Type: "
#     )


# class ChangeXYForm(forms.ModelForm):
#     class Meta:
#         model = Occurrence
#         fields = ["barcode", "item_scientific_name", "item_description"]
#     DB_id = forms.IntegerField( max_value=100000)
#     old_easting = forms.DecimalField(max_digits=12)
#     old_northing = forms.DecimalField(max_digits=12)
#     new_easting = forms.DecimalField(max_digits=12)
#     new_northing = forms.DecimalField(max_digits=12)
#
#
# class Occurrence2Biology(forms.ModelForm):
#     class Meta:
#         model = Biology
#         fields = ["barcode", "catalog_number",
#                   "basis_of_record", "item_type", "collector", "collecting_method",
#                   "field_number", "year_collected",
#                   "item_scientific_name", "item_description", "taxon", "identification_qualifier"
#                   ]
#         #fields = ['barcode', 'taxon', 'identification_qualifier']
