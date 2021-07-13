from django import forms


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
