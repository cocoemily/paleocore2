from django.core.files.base import ContentFile

from psr.models import *
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from psr.ontologies import *
import collections

import re
import os
from django.contrib.gis.geos import Point, MultiPoint
from django.contrib.gis.measure import Distance
import calendar
from datetime import datetime
import psr.ontologies
import shapefile
from django.contrib.gis.geos import GEOSGeometry
from decimal import Decimal
from mdb_parser import MDBTable

geo_filename = "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/PaleoCore-upload/geo_points/geology_21_09_20"
arch_filename = "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/PaleoCore-upload/arch_points/archaeology_21_09_20"
lo_filename = "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/PaleoCore-upload/local_points/locality_points_21_09_20"
databases = [
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Aqtasty_local_copy/aqtasty.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Aqtogai_1_local_copy/aqtogai_1.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Kyzylzhartas_local_copy/kyzylzhartas.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Marsel_ungiri_local_copy/marsel_ungiri.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Nazugum_local_copy/nazugum.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Qaraungir_local_copy/qaraungir.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Temir_2_local_copy/temir_2.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Tuttybulaq_local_copy/tuttybulaq.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Tuttybulaq_upper_local_copy/tuttybulaq_upper.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Ushbas_local_copy/ushbas.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Ushozen_local_copy/ushozen.mdb",
    "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/excavation-databases/Zhetiotau_local_copy/zhetiotau.mdb"
    ]

# def duplicate_barcodes():
#     all_occurrences = Occurrence.objects.filter(basis_of_record='FossilSpecimen')
#     barcode_list = []
#     duplicate_list = []
#     for item in all_occurrences:
#         try:
#             barcode_list.append(item.barcode)
#         except:
#             print("Error")
#     for item, count in list(collections.Counter(barcode_list).items()):
#                 if count > 1:
#                     duplicate_list.append(item)
#     return duplicate_list


# def report_duplicates():
#     dups = duplicate_barcodes()
#     for d in dups:
#         if d:
#             occs = Occurrence.objects.filter(barcode=d)
#             for o in occs:
#                 print_string = "id:{} barcode:{} item_type:{} basis:{} collector:{}".format(
#                     o.id, o.barcode, o.item_type, o.basis_of_record, o.collector
#                 )
#                 print(print_string)


# def missing_barcodes():
#     occurrences = Occurrence.objects.filter(basis_of_record='FossilSpecimen')
#     missing_list = []


# def find_mlp_duplicate_biological_barcodes():
#     all_mlp_collected_bio_occurrences = Occurrence.objects.filter(item_type__exact="Faunal").filter(basis_of_record__exact="FossilSpecimen")
#     barcode_list = []
#     duplicate_list = []
#     for item in all_mlp_collected_bio_occurrences:
#         try:
#             barcode_list.append(item.barcode)
#         except:
#             print("Error")
#     for item, count in list(collections.Counter(barcode_list).items()):
#                 if count > 1:
#                     duplicate_list.append(item)
#     return duplicate_list
#
#
# def find_mlp_duplicate_biological_catalog_numbers():
#     all_mlp_collected_bio_occurrences = Occurrence.objects.filter(item_type__exact="Faunal").filter(basis_of_record__exact="FossilSpecimen")
#     catalog_list = []
#     duplicate_list = []
#     for item in all_mlp_collected_bio_occurrences:
#         try:
#             catalog_list.append(item.catalog_number)
#         except:
#             print("Error")
#     for item, count in list(collections.Counter(catalog_list).items()):
#                 if count > 1:
#                     duplicate_list.append(item)
#     return duplicate_list
#
#
# def find_mlp_missing_coordinates():
#     all_mlp_occurrences = Occurrence.objects.all()
#     missing_coordinates_id_list=[]
#     for o in all_mlp_occurrences:
#         try: o.geom.x
#         except AttributeError:
#             missing_coordinates_id_list.append(o.id)
#     return missing_coordinates_id_list


# def update_mlp_bio(updatelist=update_tuple_list):
#     for o in updatelist:  # iterate through record tuples in list
#         cat, tax, des = o  # unpack tuple values
#         #print cat+" "+tax+" "+des  # do something with them
#
#         try:
#             occurrence = Occurrence.objects.get(catalog_number=cat)  # fetch the object with the catalog number
#             occurrence.item_scientific_name = tax  # update item scientific name
#             occurrence.item_description = des  # update item_description
#             occurrence.save()  # save updates
#         except ObjectDoesNotExist:  # handle if object is not found or is duplicate returning more than 1 match
#             print("Does Not Exist or Duplicate:"+cat)


def split_scientific_name(scientific_name):
    # split colon delimited string into list e.g. Rodentia:Muridae to ['Rodentia', 'Muridae']
    clean_name = scientific_name.strip()
    taxon_name_list = re.split('\s|:|_|,', clean_name)  # split using space, colon, underscore or comma delimeters
    taxon_name_list = [i for i in taxon_name_list if i != '']  # remove empty string resulting from extra spaces
    return clean_name, taxon_name_list


def get_identification_qualifier_from_scientific_name(scientific_name):
    clean_name, taxon_name_list = split_scientific_name(scientific_name)
    id_qual_name_list = [i.name for i in IdentificationQualifier.objects.all()]  # list of all IdQal names
    id_qual_name = [val for val in taxon_name_list if val in id_qual_name_list]  # get id_qual from taxon name list
    return IdentificationQualifier.objects.get(name__exact=id_qual_name)


def get_identification_qualifier_from_string(id_qual_string):
    """
    Function to get the id qualifier based on a string value.  Returning None as default is the wrong option here. If
    no match is found need to raise an error.
    :param id_qual_string:
    :return:
    """
    if id_qual_string in ['', ' ', None]:
        return None
    elif id_qual_string in ['cf.', 'cf', 'c.f.']:
        return IdentificationQualifier.objects.get(name='cf.')  # some fault tolerance for punctuation
    elif id_qual_string in ['aff.', 'aff', 'a.f.f.']:
        return IdentificationQualifier.objects.get(name='aff.')
    else:
        return IdentificationQualifier.objects.get(name=id_qual_string)  # last change to match novel idq
    # If no match is found ObjectDoesNotExist error is raised.


def get_taxon_from_scientific_name(scientific_name):
    """
    Function retrieves a taxon object from a colon delimited item_scientific_name string
    :param scientific_name: colon delimited item_scientific_name string, e.g. 'Rodentia:Muridae:Golunda gurai'
    :return: returns a taxon object.
    """
    clean_name, taxon_name_list = split_scientific_name(scientific_name)
    taxon_name_list_length = len(taxon_name_list)
    taxon = Taxon.objects.get(name__exact='Life')  # default taxon
    id_qual_names = [i.name for i in IdentificationQualifier.objects.all()]  # get list of id qualifier names
    # If there is no scientific name, the taxon name list will be empty and default, 'Life' will be returned
    if taxon_name_list_length >= 1:  # if there is a scientific name...
        taxon_string = taxon_name_list[-1]  # get the last element
        try:
            # This method of getting the taxon risks matching the wrong species name
            # If the taxonomy table only inlcudes Mammalia:Suidae:Kolpochoeris afarensis
            # trying to match Mammalia:Primates:Australopithecus afarensis will succeed in error
            taxon = Taxon.objects.get(name__exact=taxon_string)
        except MultipleObjectsReturned:  # if multiple taxa match a species name
            index = -2
            parent_name = taxon_name_list[index]  # get the next name in the list
            while parent_name in id_qual_names:  # if the name is an id qualifier ignore it and advance to next item
                index -=1
                parent_name = taxon_name_list[index]  # get first parent item in list that is not an id qualifier
            parent = Taxon.objects.get(name__exact=parent_name)  # find the matching parent object
            taxon = Taxon.objects.filter(name__exact=taxon_string).filter(parent=parent)[0]
        except ObjectDoesNotExist:
            print("No taxon found to match {}".format(taxon_string))
    return taxon


# def test_get_taxon_from_scientific_name(test_list=id_test_list):
#     count=0
#     for i in test_list:
#         try:
#             taxon = get_taxon_from_scientific_name(i)
#             #print '{}, {} = {}'.format(count, i, taxon)
#         except ObjectDoesNotExist:
#             print('{}, {} = {}'.format(count, i, "Does Not Exist"))
#         except MultipleObjectsReturned:
#             '{}, {} = {}'.format(count, i, 'Multiple Objects Returned')
#         count+=1


# def mlp_missing_biology_occurrences():
#     """
#     Function to identify occurrences that should also be biology but are missing from biology table
#     :return: returns a list of occurrence object ids.
#     """
#     result_list = []  # Initialize result list
#     # Biology occurrences should be all occurrences that are item_type "Faunal" or "Floral"
#     biology_occurrences = Occurrence.objects.filter(item_type__in=['Faunal', 'Floral'])
#     for occurrence in biology_occurrences:
#         try: Biology.objects.get(occurrence_ptr_id__exact=occurrence.id)  # Find matching occurrence in bio
#         except ObjectDoesNotExist:
#             result_list.append(occurrence.id)
#     return result_list


def occurrence2biology(oi, survey):
    """
    Procedure to convert an Occurrence instance to a Biology instance. The new Biology instance is given a default
    taxon = Life, and identification qualifier = None.
    :param oi: occurrence instance
    :return: returns nothing.
    """

    if oi.item_type in ['Faunal', 'Floral', 'Biological']:  # convert only faunal or floral items to Biology
        # Initiate variables
        # taxon = get_taxon_from_scientific_name(oi.item_scientific_name)
        #taxon = Taxon.objects.get(name__exact='Life')
        #id_qual = IdentificationQualifier.objects.get(name__exact='None')
        # Create a new biology object
        if survey:
            new_biology = Biology(biology_type=oi.find_type, geom=oi.geom)
        else:
            new_biology = ExcavatedBiology(biology_type=oi.type, geom=oi.geom)

        for key in list(oi.__dict__.keys()):
            new_biology.__dict__[key]=oi.__dict__[key]

        #oi.delete()
        new_biology.save()


def occurrence2archaeology(oi, survey):
    """
    Procedure to convert an Occurrence instance to an Archaeology instance.
    :param oi: occurrence instance
    :return: returns nothing
    """
    if oi.item_type in ['Artifactual', 'Archaeological']:  # convert only artifactual items to archaeology
        # Create a new archaeology object
        if survey:
            new_archaeology = Archaeology(archaeology_type=oi.find_type, geom=oi.geom)
        else:
            new_archaeology = ExcavatedArchaeology(archaeology_type=oi.type, geom=oi.geom)

        for key in list(oi.__dict__.keys()):
            new_archaeology.__dict__[key]=oi.__dict__[key]

        new_archaeology.save()
        #oi.delete()


def occurrence2geo(oi, survey):
    """
    Procedure to convert a Find (formerly Occurrence) to a Geology subclass.
    :param oi: occurrence in stance
    :return:
    """
    if oi.item_type in ['Geological']:  # convert only geological items to Geology subclass
        # Create a new Geology object
        print("Creating a new geo object for pk {}".format(oi.id))
        if survey:
            new_geo = Geology(geology_type=oi.find_type, geom=oi.geom)
        else:
            new_geo = ExcavatedGeology(geology_type=oi.type, geom=oi.geom)

        print("Copying data")
        for key in list(oi.__dict__.keys()):
            new_geo.__dict__[key]=oi.__dict__[key]
        print("Saving")
        new_geo.save()


def occurrence2aggr(oi, survey):
    """
    Procedure to convert a Find (formerly Occurrence) to a Aggregate subclass.
    :param oi: occurrence in stance
    :return:
    """
    if oi.item_type in ['Aggregate', 'Bulk Find']:  # convert only geological items to Geology subclass
        # Create a new Geology object
        print("Creating a new geo object for pk {}".format(oi.id))
        if survey:
            new_aggr = Aggregate(geom=oi.geom)
        else:
            new_aggr = ExcavatedAggregate(geom=oi.geom)

        print("Copying data")
        for key in list(oi.__dict__.keys()):
            new_aggr.__dict__[key] = oi.__dict__[key]
        print("Saving")
        new_aggr.save()


def archaeology2lithic(ai, survey):
    if ai.archaeology_type in PSR_LITHIC_VOCABULARY:
        print("Creating a new geo object for pk {}".format(ai.id))
        if survey:
            new_lithic = Lithic(geom=ai.geom)
        else:
            new_lithic = ExcavatedLithic(geom=ai.geom)

        print("Copying data")
        for key in list(ai.__dict__.keys()):
            new_lithic.__dict__[key] = ai.__dict__[key]
        print("Saving")
        new_lithic.save()


def archaeology2bone(ai, survey):
    if ai.archaeology_type in PSR_BONE_VOCABULARY:
        print("Creating a new geo object for pk {}".format(ai.id))
        if survey:
            new_bone = Bone(geom=ai.geom)
        else:
            new_bone = ExcavatedBone(geom=ai.geom)

        print("Copying data")
        for key in list(ai.__dict__.keys()):
            new_bone.__dict__[key] = ai.__dict__[key]
        print("Saving")
        new_bone.save()


def archaeology2ceramic(ai, survey):
    if ai.archaeology_type in PSR_CERAMIC_VOCABULARY:
        print("Creating a new geo object for pk {}".format(ai.id))
        if survey:
            new_cer = Ceramic(geom=ai.geom)
        else:
            new_cer = ExcavatedCeramic(geom=ai.geom)

        print("Copying data")
        for key in list(ai.__dict__.keys()):
            new_cer.__dict__[key] = ai.__dict__[key]
        print("Saving")
        new_cer.save()


def get_survey_finds():
    """
    Get Finds that are not subclassses, e.g. Find but not Biology
    :return: Returns a queryset of Find objects
    """
    all_find_ids = {f.id for f in Occurrence.objects.all()}
    subclass_ids = {f.occurrence_ptr_id for f in Biology.objects.all()} | \
                   {f.occurrence_ptr_id for f in Archaeology.objects.all()} | \
                   {f.occurrence_ptr_id for f in Geology.objects.all()}
    find_ids = all_find_ids.difference(subclass_ids)
    # return list(find_ids)
    return Occurrence.objects.filter(id__in=find_ids)


def get_excav_finds():
    """
    Get Finds that are not subclassses, e.g. Find but not Biology
    :return: Returns a queryset of Find objects
    """
    all_find_ids = {f.id for f in ExcavationOccurrence.objects.all()}
    subclass_ids = {f.excavationoccurrence_ptr_id for f in ExcavatedBiology.objects.all()} | \
                   {f.excavationoccurrence_ptr_id for f in ExcavatedArchaeology.objects.all()} | \
                   {f.excavationoccurrence_ptr_id for f in ExcavatedGeology.objects.all()} | \
                   {f.excavationoccurrence_ptr_id for f in ExcavatedAggregate.objects.all()}
    find_ids = all_find_ids.difference(subclass_ids)
    # return list(find_ids)
    return ExcavationOccurrence.objects.filter(id__in=find_ids)


def get_survey_arch():
    all_arch_ids = {f.id for f in Archaeology.objects.all()}
    subclass_ids = {f.occurrence_ptr_id for f in Lithic.objects.all()} | \
                   {f.occurrence_ptr_id for f in Bone.objects.all()} | \
                   {f.occurrence_ptr_id for f in Ceramic.objects.all()}
    find_ids = all_arch_ids.difference(subclass_ids)
    # return list(find_ids)
    return Archaeology.objects.filter(id__in=find_ids)


def get_excav_arch():
    all_arch_ids = {f.id for f in ExcavatedArchaeology.objects.all()}
    subclass_ids = {f.occurrence_ptr_id for f in ExcavatedLithic.objects.all()} | \
                   {f.occurrence_ptr_id for f in ExcavatedBone.objects.all()} | \
                   {f.occurrence_ptr_id for f in ExcavatedCeramic.objects.all()}
    find_ids = all_arch_ids.difference(subclass_ids)
    # return list(find_ids)
    return ExcavatedArchaeology.objects.filter(id__in=find_ids)


def subtype_finds(survey=True):
    if survey:
        untyped_finds = get_survey_finds()
    elif not survey:
        untyped_finds = get_excav_finds()

    for f in untyped_finds:
        if f.item_type in ['Faunal', 'Floral', 'Biological'] and f.item_scientific_name!='No Fossils At This Location':
            occurrence2biology(f, survey)
        elif f.item_type in ['Archaeological', 'Artifactual']:
            occurrence2archaeology(f, survey)
        elif f.item_type in ['Geological']:
            occurrence2geo(f, survey)
        elif f.item_type in ['Aggregate', 'Bulk Find']:
            occurrence2aggr(f, survey)
        else:
            pass


def subtype_archaeology(survey=True):
    if survey:
        untyped_finds = get_survey_arch()
    elif not survey:
        untyped_finds = get_excav_arch()

    for f in untyped_finds:
        if f.archaeology_type in PSR_BONE_VOCABULARY:
            archaeology2bone(f, survey)
        elif f.archaeology_type in PSR_LITHIC_VOCABULARY:
            archaeology2lithic(f, survey)
        elif f.item_type in PSR_CERAMIC_VOCABULARY:
            archaeology2ceramic(f, survey)
        else:
            pass


def show_duplicate_rows(data_list):
    print("\nChecking for duplicate records.")
    unique_data_list = []
    duplicates = []
    data_list_set = [list(x) for x in set(tuple(x) for x in data_list)]
    for row in data_list:
        if row not in unique_data_list:
            unique_data_list.append(row)
        else:
            duplicates.append(row)
    rowcount = 0
    for row in unique_data_list:
        row.insert(0, rowcount)
        rowcount += 1
    print("Unique rows: {} ?= Row set: {}\nDuplicate rows: {}".format(len(unique_data_list), len(data_list_set), len(duplicates)))
    return unique_data_list, duplicates, data_list_set


def set_data_list(data_list):
    return [list(x) for x in set(tuple(x) for x in data_list)]


def match_catalog_number(catalog_number_string):
    """
    Function to get occurrence objects from MLP catalog number in the form MLP-001
    the function splits the catalog number at the dash and strips leading zeros from the numberic portion of the
    catalog number. It then searches for a matching catalog number.
    :param catalog_number_string:
    :return:
    """
    cn_split = catalog_number_string.split('-')
    try:
        catalog_number_integer = int(cn_split[1])
        cleaned_catalog_number = 'MLP-' + str(catalog_number_integer)
        try:
            occurrence_obj = Biology.objects.get(catalog_number__exact=cleaned_catalog_number)
            return (True, occurrence_obj)
        except(ObjectDoesNotExist):
            return (False, catalog_number_string)
    except(IndexError):
        return (False, catalog_number_string)


def match_barcode_from_catalog_number(catalog_number_string):
    """
    Function to get occurrence objects from MLP catalog number in the form MLP-001
    the function splits the catalog number at the dash and strips leading zeros from the numberic portion of the
    catalog number. It then searches for a matching barcode number.
    :param catalog_number_string:
    :return:
    """
    cn_split = catalog_number_string.split('-')
    try:
        catalog_number_integer = int(cn_split[1])
        #cleaned_catalog_number = 'MLP-' + str(catalog_number_integer)
        try:
            occurrence_obj = Biology.objects.get(barcode__exact=catalog_number_integer)
            return (True, occurrence_obj)
        except(ObjectDoesNotExist):
            return (False, catalog_number_integer)
    except(IndexError):
        return (False, catalog_number_integer)


def match_coordinates(longitude, latitude):
    """
    Function to match an Occurrence instance given coordinates
    :param longitude: in decimal degrees
    :param latitude: in decimal degrees
    :return: returns a two element tuple. The first element is True/False indicating whether there was a single match
    The second element in None by default, or a list of queryset of matches based on coordinates.
    """

    lon = float(longitude)
    lat = float(latitude)
    pnt = Point(lon, lat)
    result = Biology.objects.filter(geom__distance_lte=(pnt, Distance(m=1)))
    match_result = (False, None)
    if (len(result)) == 1:
        match_result = (True, result)
    elif len(result) >= 1:
        match_result = (False, result)
    elif len(result) == 0:
        match_result = (False, None)
    return match_result


def match(data_list):
    print('\nMatching {} items in list'.format(len(data_list)))
    full_match_list = []
    coordinate_match_list = []
    bad_match_list = []
    for row in data_list:
        catno = row[1]  # catalog number
        lon = row[2]  # longitude
        lat = row[3]  # latitude
        basis = row[7]  # basis of record
        cat_match_result = match_catalog_number(catno)
        coord_match_result = match_coordinates(lon, lat)
        # catalog match == coordinate match (only one object)
        if cat_match_result[0] and coord_match_result[0] and cat_match_result[1] == coord_match_result[1][0]:
            match_tuple = (row, cat_match_result[1])
            full_match_list.append(match_tuple)
        # coordinate match != catalog match, e.g. because there is an old or erroneous catalog number
        elif coord_match_result[0] and not cat_match_result[0]:
            match_tuple = (row, coord_match_result[1][0])
            coordinate_match_list.append(match_tuple)
        # catalog match in coordinate match list (more than one coordinate match)
        elif cat_match_result[0] and len(coord_match_result[1]) >= 2:
            matched_object = cat_match_result[1]
            if matched_object in coord_match_result[1]:
                match_tuple = (row, matched_object)
                coordinate_match_list.append(match_tuple)
        # No cat match and multiple coord matches, see if one is human observation
        elif (not cat_match_result[0]) and (not coord_match_result[0]) and basis == 'HumanObservation':
            if coord_match_result[1]:  # if there is a coordinate match result
                if len(coord_match_result[1]) >= 2:
                    matched_objects = [i for i in coord_match_result[1] if i.catalog_number == 'MLP-0']
                    if len(matched_objects) == 1:
                        match_tuple = (row, matched_objects[0])
                        coordinate_match_list.append(match_tuple)
        else:
            # print "{}. Catalog number {} and coordinates {} {}, bad match.".format(count, catno, lon, lat)
            match_tuple = (row, None)
            bad_match_list.append(match_tuple)
            #print match_tuple

    print("Matches: {}\nCoordinate Matches: {}\nBad Matches: {}".format(len(full_match_list),
                                                                        len(coordinate_match_list),
                                                                        len(bad_match_list)))
    return full_match_list, coordinate_match_list, bad_match_list


def display_match(match_tuple):
    row, obj = match_tuple[0], match_tuple[1]

    # row data
    id = row[0]
    catalog_number = row[1]
    longitude = float(row[2])
    latitude = float(row[3])
    collector = row[4]
    date_list = row[5].split(' ')
    month = date_list[0]
    year = date_list[1]
    description = row[6]
    basis = row[7]
    sciname = row[8]
    taxon_string = row[11]
    id_qualifier = row[12]
    notes = row[10]
    taxon_obj = get_taxon_from_scientific_name(taxon_string)

    # object data
    omonth = calendar.month_name[obj.field_number.month]
    oyear = obj.field_number.year
    #                   row   id  catno  basis    lon        lat     coll   mo     yr   desc   sci   tname qual
    row_print_string = '{:3}:{:5}  {:8}  {:10}  {:10.10f} {:10.10f}  {:20}  {:8}  {:4}  {:30}  {:30}  {:30} {:5} {}\n'
    #                      bio:  id  catno  basis   lon         lat     coll   mo    yr    desc    sci  tname qual  rem
    object_print_string = '{:3}:{:5}  {:8}  {:10}  {:10.10f} {:10.10f}  {:20}  {:8}  {:4}  {:30}  {:30}  {:30} {:5} {}'

    print(object_print_string.format('bio', obj.id, obj.catalog_number,
                                     obj.basis_of_record,
                                     obj.point_x(), obj.point_y(),
                                     obj.collector, omonth, oyear,
                                     obj.item_description, obj.item_scientific_name, obj.taxon,
                                     obj.identification_qualifier,
                                     obj.remarks))
    print(row_print_string.format('row', id, catalog_number, basis,
                                  longitude, latitude,
                                  collector,
                                  month, year,
                                  description,
                                  taxon_string, taxon_obj,
                                  id_qualifier,
                                  notes))


def validate_matches(match_list, coordinate_match_list, problem_match_list):
    print("\n## Summary of Matches ##\n")
    match_no = 1

    # print "\n Catalog Number Matches\n"
    # for p in match_list:
    #     print 'Match {}'.format(match_no)
    #     match_no += 1
    #     display_match(p)
    print("\n Coordinate Matches\n")
    for p in coordinate_match_list:
        print('Match {}'.format(match_no))
        match_no += 1
        display_match(p)


def update_matches(match_list):
    print("\n## Updating Matches ##")
    counter = 0
    for m in match_list:
        row = m[0]
        obj = m[1]
        description = row[6]
        sciname = row[8]
        taxon_string = row[11]
        taxon_obj = get_taxon_from_scientific_name(taxon_string)
        id_qualifier_string = row[12]
        identifier = row[15]
        if id_qualifier_string != '':
            id_qual_obj = IdentificationQualifier.objects.get(name=id_qualifier_string)
        elif id_qualifier_string == '':
            id_qual_obj = IdentificationQualifier.objects.get(name='None')

        obj.item_scientific_name = sciname
        obj.item_description = description
        obj.taxon = taxon_obj
        obj.identification_qualifier = id_qual_obj
        obj.identified_by = identifier
        print("updated match {} cat:{}".format(row[0], row[1]))
        counter += 1
        obj.save()
    print("{} records updated successfully.".format(counter))


# def main():
#     existing, converted = update_occurrence2biology()  # convert all faunal and floral occurrences to biology
#     # import header and data list from file
#     hl, dl = import_dg_updates(file_path='/home/dnr266/paleocore/mlp/fixtures/DG_updates.txt')
#     # hl, dl = import_dg_updates()  # import header and data list from file
#     udl, du, dls = show_duplicate_rows(dl)  # check for duplicates
#     ml, cl, pl = match(udl)
#     validate_matches(ml, cl, pl)
#     update_matches(ml)
#     update_matches(cl)
#
#     return existing, converted, hl, dl, udl, du, dls, ml, cl, pl


# def find_duplicate_catalog_number(mylist):
#     unique_list = []
#     duplicate_list = []
#     for i in mylist:
#         if i not in unique_list:
#             unique_list.append(i)
#         else:
#             duplicate_list.append(i)
#     return unique_list, duplicate_list


def get_parent_name(taxon_name_list):
    index = -2
    parent_name = taxon_name_list[index]
    id_qual_names = [i.name for i in IdentificationQualifier.objects.all()]
    while parent_name in id_qual_names:
        index -= 1
        parent_name = taxon_name_list[index]
    return parent_name


def taxon_count(t):
    try:
        count = Biology.objects.filter(taxon=t).count()
    except:
        count = None
    return count


def get_taxa_counts(rank=None):
    """
    function to generate taxonomic lists based on Biology instances for a project
    :param rank:
    :return: Returns a list of tuples containing the taxon and taxon rank,
    e.g. [(<Life>,<root>), (<Animalia>, <Kingdom>), ... ]
    """

    biology_objects = Biology.objects.all()
    taxon_set = set([b.taxon for b in biology_objects])
    taxon_object_list = [(t, t.rank, taxon_count(t)) for t in taxon_set]
    if rank:
        pass
    return taxon_object_list


def get_taxa():
    """
    Get a list of distinct taxon objects for biology instances
    :return: Returns a list
    """
    return [b.taxon for b in Biology.objects.distinct('taxon')]


html_escape_table = {
    "&": "&amp;",
    # ">": "&gt;",
    # "<": "&lt;",
    # "'": "&apos;",
    # '"': "&quot;",
}


def html_escape(text):
    """
    Escape unsafe characters from text strings and replace with html
    :param text:
    :return:
    """
    return "".join(html_escape_table.get(c, c) for c in text)


def import_pre2020_geology_shapefile(filename):
    sf = shapefile.Reader(filename)
    sr = sf.shapeRecords()
    for r in sr:
        if r.record["Item Type"] in ("Geosample") :
            psr_g = Occurrence(
                basis_of_record=r.record["Basis Of R"],
                item_count=r.record["Item Count"],
                find_type=r.record["Item Type"],
                item_description=r.record["Descriptio"],
                collecting_method=r.record["Collecting"],
                field_id=r.record["Name"],
                collection_remarks=r.record["Remarks"]
            )
            # set item type code
            if psr_g.find_type in PSR_ARCHAEOLOGY_VOCABULARY:
                psr_g.item_type = "Archaeological"
            elif psr_g.find_type in PSR_BIOLOGY_VOCABULARY:
                psr_g.item_type = "Biological"
            elif psr_g.find_type in PSR_GEOLOGY_VOCABULARY:
                psr_g.item_type = "Geological"
            else:
                pass

            #set point
            if r.shape.shapeType is 1:  # point
                coords = r.shape.points[0]
                geom = GEOSGeometry("POINT(" + str(coords[0]) + " " + str(coords[1]) + ")", 4326)
            psr_g.point = geom
            psr_g.geom = geom
            # set geological context
            try:
                psr_g.geological_context = GeologicalContext.objects.get(name=r.record["Locality"])
            except:
                psr_g.geological_context = GeologicalContext.objects.get_or_create(name=r.record["Locality"], geom=geom, point=geom)[0]

        else:
            psr_g = GeologicalContext(
                basis_of_record = r.record["Basis Of R"],
                collecting_method= r.record["Collecting"],
                name = r.record["Name"],
                context_type = r.record["Item Type"],
                description = r.record["Descriptio"],
                dip = r.record["Dip"],
                strike = r.record["Strike"],
                texture = r.record["Texture"],
                color = r.record["Color"],
                context_remarks= r.record["Remarks"],
                rockfall_character = r.record["Rockfall C"],
                sediment_character = r.record["Sediment C"],
                slope_character= r.record["Slope Char"],
                speleothem_character= r.record["Speleothem"],
                cave_mouth_character= r.record["Cave Mouth"],
                geology_type = r.record["Geology Ty"]
            )

            if r.record["Height"] not in ("", None):
                psr_g.height = Decimal(r.record["Height"])
            if r.record["Width"] not in ("", None):
                psr_g.width = Decimal(r.record["Width"])
            if r.record["Depth"] not in ("", None):
                psr_g.depth = Decimal(r.record["Depth"])

            if r.record["Sediment P"] in ('-None Selected-'):
                psr_g.sediment_presence = None
            else:
                psr_g.sediment_presence = r.record["Sediment P"]

            if r.shape.shapeType is 1:  # point
                coords = r.shape.points[0]
                geom = GEOSGeometry("POINT(" + str(coords[0]) + " " + str(coords[1]) + ")", 4326)
            # elif r.shape.shapeType is 5: #polygon
            # elif r.shape.shapeType is 8: #multipoint
            psr_g.geom = geom
            psr_g.point = geom

        if r.record["Date Recor"] is not "":
            if "at" in r.record["Date Recor"]:
                psr_g.date_collected = datetime.strptime(r.record["Date Recor"], '%d. %b %Y at %H:%M')
            elif "," in r.record["Date Recor"]:
                psr_g.date_collected = datetime.strptime(r.record["Date Recor"], '%d. %b %Y, %H:%M')
            else:
                psr_g.date_collected = datetime.strptime(r.record["Date Recor"], '%d. %b %Y')
        else:
            psr_g.date_collected = None

        if r.record["Recorded B"] not in ('-None Selected-', "", None):
            name=r.record["Recorded B"].split(" ")
            psr_g.recorded_by=Person.objects.get_or_create(last_name=name[1], first_name=name[0])[0]

        psr_g.last_import = True
        psr_g.save()

        photodir = "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/PaleoCore-upload/geo_points"
        photonames = r.record["Photo"].split(",")
        upload_pictures(photonames, psr_g, photodir)


def import_pre2020_archaeology_shapefile(filename):
    sf = shapefile.Reader(filename)
    sr = sf.shapeRecords()
    for r in sr: #iterate through each record
        if r.record["Item Type"] in ("Caves"):
            psr_a = GeologicalContext(
                basis_of_record=r.record["Basis Of R"],
                collecting_method=r.record["Collecting"],
                name=r.record["Name"],
                context_type=r.record["Item Type"],
                description=r.record["Descriptio"],
                #dip=r.record["Dip"],
                #strike=r.record["Strike"],
                #texture=r.record["Texture"],
                #color=r.record["Color"],
                context_remarks=r.record["Remarks"],
                rockfall_character=r.record["Rockfall C"],
                sediment_character=r.record["Sediment C"],
                slope_character=r.record["Slope Char"],
                speleothem_character=r.record["Speleothem"],
                cave_mouth_character=r.record["Cave Mouth"],
                #geology_type=r.record["Geology Ty"]
            )

            if r.record["Height"] not in ("", None):
                psr_a.height = Decimal(r.record["Height"])
            if r.record["Width"] not in ("", None):
                psr_a.width = Decimal(r.record["Width"])
            if r.record["Depth"] not in ("", None):
                psr_a.depth = Decimal(r.record["Depth"])

            if r.record["Sediment P"] in ('-None Selected-'):
                psr_a.sediment_presence = None
            else:
                psr_a.sediment_presence = r.record["Sediment P"]

            if r.shape.shapeType is 1:  # point
                coords = r.shape.points[0]
                geom = GEOSGeometry("POINT(" + str(coords[0]) + " " + str(coords[1]) + ")", 4326)
            # elif r.shape.shapeType is 5: #polygon
            # elif r.shape.shapeType is 8: #multipoint
            psr_a.geom = geom
            psr_a.point = geom

        else:
            psr_a = Occurrence(
                basis_of_record=r.record["Basis Of R"],
                item_count=r.record["Item Count"],
                find_type=r.record["Item Type"],
                item_description=r.record["Descriptio"],
                #collector=r.record["Identified"],
                #finder=r.record["Identified"],
                collecting_method=r.record["Collecting"],
                field_id=r.record["Name"],
                collection_remarks=r.record["Remarks"]
            )
            #set item type code
            if psr_a.find_type in PSR_ARCHAEOLOGY_VOCABULARY:
                psr_a.item_type = "Archaeological"
            elif psr_a.find_type in PSR_BIOLOGY_VOCABULARY:
                psr_a.item_type = "Biological"
            elif psr_a.find_type in PSR_GEOLOGY_VOCABULARY:
                psr_a.item_type = "Geological"
            else:
                pass

            # set point
            if r.shape.shapeType is 1:  # point
                coords = r.shape.points[0]
                geom = GEOSGeometry("POINT(" + str(coords[0]) + " " + str(coords[1]) + ")", 4326)
            psr_a.point = geom
            psr_a.geom = geom

            # set geological context
            try:
                psr_a.geological_context = GeologicalContext.objects.get(name=r.record["Locality"])
            except:
                psr_a.geological_context = GeologicalContext.objects.get_or_create(name=r.record["Locality"], geom=geom, point=geom)[0]

            # set people
            if r.record["Identified"] not in ('-None Selected-', "", None):
                name1 = r.record["Identified"].split(" ")
                psr_a.found_by = Person.objects.get_or_create(last_name=name1[1], first_name=name1[0])[0]
                psr_a.collector=r.record["Identified"]
                psr_a.finder=r.record["Identified"]


        if r.record["Date Recor"] not in ("", None):
            if "at" in r.record["Date Recor"]:
                psr_a.date_collected = datetime.strptime(r.record["Date Recor"], '%d. %b %Y at %H:%M')
            elif "," in r.record["Date Recor"]:
                psr_a.date_collected = datetime.strptime(r.record["Date Recor"], '%d. %b %Y, %H:%M')
            else:
                psr_a.date_collected = datetime.strptime(r.record["Date Recor"], '%d. %b %Y')
        else:
            psr_a.date_collected = None

        if r.record["Recorded B"] not in ('-None Selected-', "", None):
            name=r.record["Recorded B"].split(" ")
            psr_a.recorded_by=Person.objects.get_or_create(last_name=name[1], first_name=name[0])[0]

        psr_a.last_import = True
        psr_a.save()  # last step to add it to the database

        photodir = "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/PaleoCore-upload/arch_points"
        photonames = r.record["Photo"].split(",")
        upload_pictures(photonames, psr_a, photodir)


def import_pre2020_locality_points_shapefile(filename):
    sf = shapefile.Reader(filename)
    sr = sf.shapeRecords()
    for r in sr:  # iterate through each record
        psr_l = Occurrence(
            find_type=r.record["Type"],
            item_description=r.record["Descriptio"],
            field_id=r.record["Name"]
        )
        # set item type code
        if psr_l.find_type in PSR_ARCHAEOLOGY_VOCABULARY:
            psr_l.item_type = "Archaeological"
        elif psr_l.find_type in PSR_BIOLOGY_VOCABULARY:
            psr_l.item_type = "Biological"
        elif psr_l.find_type in PSR_GEOLOGY_VOCABULARY:
            psr_l.item_type = "Geological"
        else:
            pass

        # set point
        if r.shape.shapeType is 1:  # point
            coords = r.shape.points[0]
            geom = GEOSGeometry("POINT (" + str(coords[0]) + " " + str(coords[1]) + ")", 4326)
        psr_l.point = geom
        psr_l.geom = geom

        # set geological context
        try:
            psr_l.geological_context = GeologicalContext.objects.get(name=r.record["Locality"])
        except:
            psr_l.geological_context = GeologicalContext.objects.get_or_create(name=r.record["Locality"], geom=geom, point=geom)[0]

        psr_l.last_import = True
        psr_l.save()  # last step to add it to the database

        photodir = "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/PaleoCore-upload/landscape_observations"
        photonames = r.record["Photos"].split(",")
        upload_pictures(photonames, psr_l, photodir)


#photodir = "/Users/emilycoco/Desktop/NYU/Kazakhstan/PSR-Paleo-Core/PaleoCore-upload/geo_points"
def upload_pictures(photonames, obj, photodir):
    if not 'N/A' in photonames[0]:
        for p in photonames:
            if os.path.isfile(os.path.join(photodir, p)):
                f = open(os.path.join(photodir, p), 'rb')
                upload_dir = Image._meta.get_field('image').upload_to
                name = os.path.join(upload_dir, str(obj.id) + '_' + p)
                im = Image(description=name)
                if type(obj) is Occurrence:
                    im.occurrence = Occurrence.objects.get_or_create(id = obj.id)[0]
                    im.locality = obj.geological_context
                elif type(obj) is GeologicalContext:
                    im.locality = GeologicalContext.objects.get_or_create(id = obj.id)[0]
                im.image.save(name, ContentFile(f.read()))
                im.save()


locality_names = {
    "Kyzylzhartas": "Qyzyljartas",
    "Tuttybulaq Upper": "Tuttybulaq 2",
    "Zhetiotau": "Jetiotau Cave"
}


def parse_mdb(file_path, locality_names=locality_names):
    dbname = file_path.split("/")
    db = dbname[dbname.__len__()-1]
    name = db.replace("_", ".").split(".")

    if name.__len__() == 2:
        lname = name[0].capitalize()
    else:
        if name[1].isdigit() :
            lname = name[0].capitalize() + " " + name[1]
        else:
            lname = name[0].capitalize() + " " + name[1].capitalize()

    print(lname)

    try:
        locality = GeologicalContext.objects.get(name=lname)
    except:
        if lname in locality_names:
            lname2 = locality_names[lname]
            locality = GeologicalContext.objects.get(name=lname2)
        elif not any(char.isdigit() for char in lname):
            lname2 = lname + " 1"
            locality = GeologicalContext.objects.get(name=lname2)

    context = MDBTable(file_path, "Context")
    xyz = MDBTable(file_path, "xyz")
    units = MDBTable(file_path, "EDM_Units")

    for u in units:
        psr_eu = ExcavationUnit.objects.get_or_create(unit=u[0], geological_context=locality)[0]
        psr_eu.extent = MultiPoint(Point(int(u[2]), int(u[4]), srid=-1), Point(int(u[3]), int(u[5]), srid=-1), srid=-1)
        psr_eu.save()

    for obj in context:
        un = ExcavationUnit.objects.get_or_create(unit=obj[0], geological_context=locality)[0]
        psr_eo = ExcavationOccurrence.objects.get_or_create(geological_context=locality, unit=un, field_id=obj[1])[0]
        psr_eo.level = obj[2]
        psr_eo.type = obj[3]
        psr_eo.excavator = obj[4]
        psr_eo.cat_number = obj[0] + " " + obj[1]

        #TODO create method for pulling Person foreign key

        # set item type code for subtyping
        if psr_eo.type in PSR_ARCHAEOLOGY_VOCABULARY:
            psr_eo.item_type = "Archaeological"
        elif psr_eo.type in PSR_BIOLOGY_VOCABULARY:
            psr_eo.item_type = "Biological"
        elif psr_eo.type in PSR_GEOLOGY_VOCABULARY:
            psr_eo.item_type = "Geological"
        elif psr_eo.type in PSR_AGGREGATE_VOCABULARY:
            psr_eo.item_type = "Aggregate"
        else:
            pass

        psr_eo.last_import = True
        psr_eo.save()

    for p in xyz:
        un = ExcavationUnit.objects.get_or_create(unit=p[0], geological_context=locality)[0]
        eo = ExcavationOccurrence.objects.get_or_create(unit=un, field_id=p[1], geological_context=locality)
        obj = eo[0]
        is_new = eo[1]
        obj.prism = p[3] ## TODO multiple different prism heights for different points
        if (p[7] + " " + p[8]) is not " ":
            obj.date_collected = datetime.strptime(p[7] + " " + p[8], '%m/%d/%Y %I:%M:%S %p')

        if not is_new:
            if obj.point is not None:
                new_point = Point(float(p[4]), float(p[5]), float(p[6]), srid=-1)
                points = [pt for pt in obj.point]
                if new_point not in points:
                    points.append(new_point)
                    obj.point = MultiPoint(points, srid=-1)
            else:
                obj.point = MultiPoint(Point(float(p[4]), float(p[5]), float(p[6]), srid=-1))
        else:
            obj.point = MultiPoint(Point(float(p[4]), float(p[5]), float(p[6]), srid=-1))

        obj.save()




