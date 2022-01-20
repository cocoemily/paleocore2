from django.shortcuts import render
import os
from fastkml import kml, Placemark, Folder, Document
from lxml import etree
from datetime import datetime
from django.contrib.gis.geos import GEOSGeometry
from pygeoif import geometry
from zipfile import ZipFile
import tempfile

# Django Libraries
from django.conf import settings
from django.views import generic
from django.http import HttpResponse
#from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from dateutil.parser import parse
from django.core.files.base import ContentFile

# App Libraries
from .models import Occurrence, Biology, Archaeology, Geology, Taxon, IdentificationQualifier
from .forms import *
from .utilities import *
from .ontologies import *  # import vocabularies and choice lists


class ImportShapefile(generic.FormView):
    template_name = "admin/psr/import_file.html"
    form_class = UploadShapefile
    context_object_name = 'upload'
    success_url = '../?last_import__exact=1'

    def get_import_shp_file(self):
        return self.request.FILES['shpfileUpload']

    def get_import_dbf_file(self):
        return self.request.FILES['shpfileDataUpload']

    def get_photos(self):
        return self.request.FILES.getlist('photoUpload')

    def get_import_file_path(self):
        import_file = self.get_import_file()
        file_extension = self.get_import_file_extension()  # get the file extension
        file_path = os.path.join(settings.MEDIA_ROOT)
        return file_path + "/" + import_file.name

    def get_import_file_extension(self):
        import_file = self.get_import_file()
        import_file_name = import_file.name
        return import_file_name[import_file_name.rfind('.') + 1:]  # get the file extension

    def import_shapefile_data(self):
        shp = self.get_import_shp_file()
        tempshp, tempshpname = tempfile.mkstemp()
        try:
            for chunk in shp.chunks():
                os.write(tempshp, chunk)
        except:
            raise Exception("Problem with input file %s" % shp.name)
        finally:
            os.close(tempshp)

        dbf = self.get_import_dbf_file()
        tempdbf, tempdbfname = tempfile.mkstemp()
        try:
            for chunk in dbf.chunks():
                os.write(tempdbf, chunk)
        except:
            raise Exception("Problem with input file %s" % dbf.name)
        finally:
            os.close(tempdbf)

        if "geologicalcontext" in self.request.path.split("/"):
            print("GeoContext")
            GeologicalContext.objects.all().update(last_import=False)
            import_geo_contexts(tempshpname, tempdbfname, self.get_photos())

        #elif "occurrence" in self.request.path.split("/"):
        else:
            print("Occurrence")
            Occurrence.objects.all().update(last_import=False)
            import_survey_occurrences(tempshpname, tempdbfname)
            subtype_archaeology(survey=True)

    def form_valid(self, form):
        self.import_shapefile_data()
        return super(ImportShapefile, self).form_valid(form)


class ImportShapefileDirectory(generic.FormView):
    template_name = "admin/psr/import_file.html"
    form_class = UploadShapefileDirectory
    context_object_name = 'upload'
    success_url = '../?last_import__exact=1'

    def get_import_files(self):
        return self.request.FILES.getlist('shapefileUpload')

    def get_shp_file(self):
        for f in self.get_import_files():
            if f.name.endswith(".shp"):
                return f

    def get_dbf_file(self):
        for f in self.get_import_files():
            if f.name.endswith(".dbf"):
                return f

    def get_photos(self):
        img = []
        for f in self.get_import_files():
            if f.name.endswith(".jpg"):
                img.append(f)

        return img

    def import_shapefile_data(self):
        shp = self.get_shp_file()
        tempshp, tempshpname = tempfile.mkstemp()
        try:
            for chunk in shp.chunks():
                os.write(tempshp, chunk)
        except:
            raise Exception("Problem with input file %s" % shp.name)
        finally:
            os.close(tempshp)

        dbf = self.get_dbf_file()
        tempdbf, tempdbfname = tempfile.mkstemp()
        try:
            for chunk in dbf.chunks():
                os.write(tempdbf, chunk)
        except:
            raise Exception("Problem with input file %s" % dbf.name)
        finally:
            os.close(tempdbf)

        if "geologicalcontext" in self.request.path.split("/"):
            print("GeoContext")
            GeologicalContext.objects.all().update(last_import=False)
            import_geo_contexts(tempshpname, tempdbfname, self.get_photos())

        # elif "occurrence" in self.request.path.split("/"):
        else:
            print("Occurrence")
            Occurrence.objects.all().update(last_import=False)
            import_survey_occurrences(tempshpname, tempdbfname, self.get_photos())

    def form_valid(self, form):
        self.import_shapefile_data()
        return super(ImportShapefileDirectory, self).form_valid(form)


class ImportAccessDatabase(generic.FormView):
    template_name = "admin/psr/import_file.html"
    form_class = UploadMDB
    context_object_name = 'upload'
    success_url = '../?last_import__exact=1'

    def get_import_file(self):
        return self.request.FILES['mdbUpload']

    def get_import_file_path(self):
        import_file = self.get_import_file()
        file_extension = self.get_import_file_extension()  # get the file extension
        file_path = os.path.join(settings.MEDIA_ROOT)
        return file_path + "/" + import_file.name

    def get_import_file_extension(self):
        import_file = self.get_import_file()
        import_file_name = import_file.name
        return import_file_name[import_file_name.rfind('.') + 1:]  # get the file extension

    def import_excavated_instances(self):
        file = self.get_import_file()
        fsplit = file.name.split(".")
        name = fsplit[0].split("_")

        if name.__len__() == 1:
            lname = name[0].capitalize()
        else:
            if name[1].isdigit():
                lname = name[0].capitalize() + " " + name[1]
            else: #will there ever be geological context names with more than three?
                lname = name[0].capitalize() + " " + name[1].capitalize()

        ExcavationOccurrence.objects.all().update(last_import=False)
        parse_mdb(file.temporary_file_path(), lname)
        subtype_finds(survey = False)
        subtype_archaeology(survey = False)

    def form_valid(self, form):
        self.import_excavated_instances()
        return super(ImportAccessDatabase, self).form_valid(form)


class ImportJSON(generic.FormView):
    template_name = "admin/psr/import_file.html"
    form_class = UploadJSON
    context_object_name = 'upload'
    success_url = '../?last_import__exact=1'

    def get_import_file(self):
        return self.request.FILES['jsonUpload']

    def import_geo_contexts(self):
        GeologicalContext.objects.all().update(last_import=False)
        import_geo_context_from_json(self.get_import_file())

    def form_valid(self, form):
        self.import_geo_contexts()
        return super(ImportJSON, self).form_valid(form)
