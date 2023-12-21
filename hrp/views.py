import os
from django.conf import settings
from django.views import generic
from django.contrib import messages
from django.contrib.gis.geos import GEOSGeometry
from django.core.files.base import ContentFile
from .serialziers import BiologySerializer, TaxonRankSerializer
from .models import Occurrence, Biology, Archaeology, Geology, Person, TaxonRank
from .forms import UploadKMLForm
from .utilities import match_taxon, match_element
from rest_framework import viewsets
from rest_framework import permissions

from fastkml import kml
from fastkml import Placemark, Folder, Document
from lxml import etree
from datetime import datetime
from dateutil.parser import parse
from zipfile import ZipFile


class ImportKMZ(generic.FormView):
    template_name = 'admin/projects/import_kmz.html'
    form_class = UploadKMLForm
    context_object_name = 'upload'
    success_url = '../?last_import__exact=1'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        # TODO parse the kml file more smartly to locate the first placemark and work from there.
        kml_file_upload = self.request.FILES['kmlfileUpload']  # get a handle on the file

        kml_file_upload_name = self.request.FILES['kmlfileUpload'].name  # get the file name
        # kml_file_name = kml_file_upload_name[:kml_file_upload_name.rfind('.')]  # get the file name no extension
        kml_file_extension = kml_file_upload_name[kml_file_upload_name.rfind('.')+1:]  # get the file extension

        kml_file_path = os.path.join(settings.MEDIA_ROOT)

        # Define a routine for importing Placemarks from a list of placemark elements
        def import_placemarks(kml_placemark_list):
            """
            A procedure that reads a KML placemark list and saves the data into the django database
            :param kml_placemark_list:
            :return:
            """
            occurrence_count, archaeology_count, biology_count, geology_count = [0, 0, 0, 0]
            Occurrence.objects.all().update(last_import=False)  # Toggle off all last imports
            for o in kml_placemark_list:

                # Check to make sure that the object is a Placemark, filter out folder objects
                if type(o) is Placemark:
                    # Step 1 - parse the xml and copy placemark attributes to a dictionary
                    table = etree.fromstring(o.description)  # get the table element with all the data from the xml.
                    attributes = table.xpath("//text()|//img")  # get all text values and image tags from xml string
                    # TODO test attributes is even length
                    # Create a diction ary from the attribute list. The list has key value pairs as alternating
                    # elements in the list, the line below takes the first and every other elements and adds them
                    # as keys, then the second and every other element and adds them as values.
                    # e.g.
                    # attributes[0::2] = ["Basis of Record", "Time", "Item Type" ...]
                    # attributes[1::2] = ["Collection", "May 27, 2017, 10:12 AM", "Faunal" ...]
                    # zip creates a list of tuples  = [("Basis of Record", "Collection), ...]
                    # which is converted to a dictionary.
                    attributes_dict = dict(zip(attributes[0::2], attributes[1::2]))

                    # Step 2 - Create a new Occurrence object (or subtype)
                    new_occ = None
                    # Determine the appropriate subtype and initialize
                    item_type = attributes_dict.get("Item Type")
                    occurrence_count += 1
                    if item_type in ("Artifact", "Artifactual", "Archeology", "Archaeological"):
                        new_occ = Archaeology()
                        archaeology_count += 1
                    elif item_type in ("Faunal", "Fauna", "Floral", "Flora"):
                        new_occ = Biology()
                        biology_count +=1
                    elif item_type in ("Geological", "Geology"):
                        new_occ = Geology()
                        geology_count += 1

                    # Step 3 - Copy attributes from dictionary to Occurrence object, validate as we go.
                    # Improve by checking each field to see if it has a choice list. If so validate against choice
                    # list.

                    # Verbatim Data - save a verbatim copy of the original kml placemark attributes.
                    new_occ.verbatim_kml_data = attributes

                    # Validate Basis of Record
                    if attributes_dict.get("Basis Of Record") in ("Fossil", "FossilSpecimen", "Collection"):
                        new_occ.basis_of_record = "Collection"
                    elif attributes_dict.get("Basis Of Record") in ("Observation", "HumanObservation"):
                        new_occ.basis_of_record = "Observation"

                    # Validate Item Type
                    item_type = attributes_dict.get("Item Type")
                    if item_type in ("Artifact", "Artifactual", "Archeology", "Archaeological"):
                        new_occ.item_type = "Artifactual"
                    elif item_type in ("Faunal", "Fauna"):
                        new_occ.item_type = "Faunal"
                    elif item_type in ("Floral", "Flora"):
                        new_occ.item_type = "Floral"
                    elif item_type in ("Geological", "Geology"):
                        new_occ.item_type = "Geological"

                    # Date Recorded
                    try:
                        # parse the time
                        new_occ.date_recorded = parse(attributes_dict.get("Time"))
                        # set the year collected form field number
                        new_occ.year_collected = new_occ.date_recorded.year
                    except ValueError:
                        # If there's a problem getting the fieldnumber, use the current date time and set the
                        # problem flag to True.
                        new_occ.date_recorded = datetime.now()
                        new_occ.problem = True
                        try:
                            error_string = "Upload error, missing field number, using current date and time instead."
                            new_occ.problem_comment = new_occ.problem_comment + " " + error_string
                        except TypeError:
                            new_occ.problem_comment = error_string

                    # Process point, comes in as well known text string
                    # Assuming point is in GCS WGS84 datum = SRID 4326
                    pnt = GEOSGeometry("POINT (" + str(o.geometry.x) + " " + str(o.geometry.y) + ")", 4326)  # WKT
                    new_occ.geom = pnt

                    scientific_name_string = attributes_dict.get("Scientific Name")
                    new_occ.item_scientific_name = scientific_name_string
                    if new_occ.item_scientific_name:
                        match, match_count, match_list = match_taxon(new_occ)
                        if match and match_count == 1:
                            new_occ.taxon = match_list[0]

                    new_occ.item_description = attributes_dict.get("Description")
                    if new_occ.item_description:
                        match, match_count, match_list = match_element(new_occ)
                        if match and match_count ==1:
                            new_occ.element = new_occ.item_description.lower()

                    #######################
                    # NON-REQUIRED FIELDS #
                    #######################
                    new_occ.barcode = attributes_dict.get("Barcode")
                    new_occ.item_number = new_occ.barcode
                    new_occ.collection_remarks = attributes_dict.get("Collecting Remarks")
                    new_occ.geology_remarks = attributes_dict.get("Geology Remarks")

                    new_occ.collecting_method = attributes_dict.get("Collection Method")
                    finder_string = attributes_dict.get("Finder")
                    new_occ.finder = finder_string
                    # import person object, validated against look up data in Person table
                    new_occ.finder_person, created = Person.objects.get_or_create(name=finder_string)

                    collector_string = attributes_dict.get("Collector")
                    new_occ.collector = collector_string
                    # import person object, validated against look up data in Person table
                    new_occ.collector_person, created = Person.objects.get_or_create(name=collector_string)

                    new_occ.individual_count = attributes_dict.get("Count")

                    if attributes_dict.get("In Situ") in ('No', "NO", 'no'):
                        new_occ.in_situ = False
                    elif attributes_dict.get("In Situ") in ('Yes', "YES", 'yes'):
                        new_occ.in_situ = True

                    if attributes_dict.get("Ranked Unit") in ('No', "NO", 'no'):
                        new_occ.ranked = False
                    elif attributes_dict.get("Ranked Unit") in ('Yes', "YES", 'yes'):
                        new_occ.ranked = True

                    unit_found_string = attributes_dict.get("Unit Found")
                    unit_likely_string = attributes_dict.get("Unit Likely")
                    new_occ.analytical_unit_found = unit_found_string
                    new_occ.analytical_unit_likely = unit_likely_string
                    new_occ.analytical_unit_1 = attributes_dict.get("Unit 1")
                    new_occ.analytical_unit_2 = attributes_dict.get("Unit 2")
                    new_occ.analytical_unit_3 = attributes_dict.get("Unit 3")

                    # import statigraphy object, validate against look up data in Stratigraphy table
                    # HPR does  not have a Stratigraphy table for tracking stratigraphic units.
                    # new_occ.unit_found, created = StratigraphicUnit.objects.get_or_create(name=unit_found_string)
                    # new_occ.unit_likly, created = StratigraphicUnit.objects.get_or_create(name=unit_likely_string)

                    # Save Occurrence before saving media. Need id to rename media files
                    new_occ.last_import = True
                    new_occ.save()

                    # Save image
                    if kml_file_extension.lower() == "kmz":
                        # grab image names from XML
                        image_names = table.xpath("//img/@src")
                        # grab the name of the first image
                        # Future: add functionality to import multiple images
                        if image_names and len(image_names) == 1:  # This will break if image_names is None
                            image_name = image_names[0]
                            # Check that the image name is in the kmz file list
                            kmz_file.filenames = [f.orig_filename for f in kmz_file.filelist]
                            if image_name in kmz_file.filenames:
                                # etch the kmz image file object, this is a ZipInfo object not a File object
                                image_file_obj = next(f for f in kmz_file.filelist if f.orig_filename == image_name)
                                # fetch the upload directory from the model definition
                                upload_dir = Biology._meta.get_field('image').upload_to
                                # update image name to include upload path and occurrence id
                                # e.g. /uploads/images/lgrp/14775_188.jpg
                                new_image_name = os.path.join(upload_dir, str(new_occ.id)+'_'+image_name)
                                # Save the image
                                new_occ.image.save(new_image_name, ContentFile(kmz_file.read(image_file_obj)))

                elif type(o) is not Placemark:
                    raise IOError("KML File is badly formatted")
            if occurrence_count == 1:
                message_string = '1 occurrence'
            if occurrence_count > 1:
                message_string = '{} occurrences'.format(occurrence_count)
            messages.add_message(self.request, messages.INFO,
                                 'Successfully imported {} occurrences'.format(message_string))

        kml_file = kml.KML()
        if kml_file_extension == "kmz":
            kmz_file = ZipFile(kml_file_upload, 'r')
            kml_document = kmz_file.open('doc.kml', 'r').read()
        else:
            # read() loads entire file as one string
            kml_document = open(kml_file_path + "/" + kml_file_upload_name, 'r').read()

        kml_file.from_string(kml_document)  # pass contents of kml string to kml document instance for parsing

        # get the top level features object (this is essentially the layers list)
        level1_elements = list(kml_file.features())

        # Check that the kml file is well-formed with a single document element.
        if len(level1_elements) == 1 and type(level1_elements[0]) == Document:
            document = level1_elements[0]

            #  If well-formed document, check if the file has folders, which correspond to layers
            level2_elements = list(document.features())
            if len(level2_elements) == 1 and type(level2_elements[0]) == Folder:
                folder = level2_elements[0]

                #  If a single folder is present import placemarks from that folder
                #  Get features from the folder
                level3_elements = list(folder.features())
                #  Check that the features are Placemarks. If they are, import them
                if len(level3_elements) >= 1 and type(level3_elements[0]) == Placemark:
                    placemark_list = level3_elements
                    import_placemarks(placemark_list)

            elif len(level2_elements) >= 1 and type(level2_elements[0]) == Placemark:
                placemark_list = level2_elements
                import_placemarks(placemark_list)

        return super(ImportKMZ, self).form_valid(form)


# API Viewsets
class BiologyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Fossils to be viewed
    """

    queryset = Biology.objects.all()
    serializer_class = BiologySerializer
    permission_classes = [permissions.IsAuthenticated]


class TaxonRankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Taxon Ranks to be viewed
    """
    queryset = TaxonRank.objects.all()
    serializer_class = TaxonRankSerializer
    # permission_classes = [permissions.IsAuthenticated]
