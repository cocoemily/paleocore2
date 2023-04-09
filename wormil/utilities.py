from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
import json
import projects.utilities as utils
from .models import *
import pandas as pd


# Import file location
localities_file_path = '/Users/dreed/Desktop/wormil_localities_cleaned.xlsx'
fossils_file_path = '/Users/dreed/Desktop/wormil_fossils_cleaned.xlsx'


def write_row_to_verbatim(df, app_label, model, field_name):
    """
    Read a panda datafram and write each row of data into the verbatim field of a new object.
    :param df: The input pandas dataframe
    :param app_label: The app
    :param model: The app model
    :param field_name: The field in which to write the verbatim data
    :return:
    """
    # Get the model class for the app
    model_class = ContentType.objects.get(app_label=app_label, model=model).model_class()
    # iterate through the DF and convert each row to a dictionary
    for row_json in df.to_json('records'):
        # row_json = json.dumps(row_dict)
        # these three lines below can probably be replaced with a single create command
        new_instance = model_class()  # create a new instance
        setattr(new_instance, field_name, row_json)  # update the verbatim field with the json data
        new_instance.save()  # save the instance to the DB


def import_localities(source_path=localities_file_path):
    xls = pd.ExcelFile(source_path)
    df = xls.parse(xls.sheet_names[0])
    row_index = 1
    for i in df.index:
        #row_json = json.dumps(row_dict)
        #row_json = row_json.replace('NaN', '')
        new_locality = Locality()
        new_locality.verbatim_row_data = df.loc[i].to_json()
        new_locality.save()

    for locality in Locality.objects.all():
        data = json.loads(locality.verbatim_row_data)
        locality_id = data['LocalityDesignation']
        print(f"Processing id: {locality.id}, row: {row_index}, locality_id: {locality_id}")
        locality.locality_id = locality_id
        locality.collection_code = data['CollectionCode']
        locality.name = data['LocalityNameCommon']
        # locality.formation = data['Geological Formation']
        # locality.member = data['Geological Member']
        locality.bed = data['Stratigraphic Interval']
        locality.verbatim_age_ma = data['Estimated age in Myr']
        ea = data['earliest_age']
        if pd.isna(ea):
            ea = None
        locality.earliest_age_ma = ea
        la = data['latest_age']
        if pd.isna(la):
            la = None
        locality.latest_age_ma = la
        locality.age_protocol = data['AgeBasis']
        year = data['DiscoveryYear']
        if pd.isna(year):
            year = None
        locality.year_established = year
        locality.dimension_ew = data['Dimension_E|W']
        locality.dimension_ns = data['Dimension_N|S']
        locality.remarks = data['Locality Description']
        locality.locality_boundary_east = data['Locality_boundary_East']
        locality.locality_boundary_north = data['Locality_boundary_North']
        locality.locality_boundary_south = data['Locality_boundary_South']
        locality.locality_boundary_west = data['Locality_boundary_West']
        locality.macrobotanical_evidence = data['Macrobotanical evidence']
        locality.archaeological_evidence = data['Archaeological evidence']
        locality.uncollected_taxa = data['Uncollected taxa present']
        elevation = data['elevation_meters']
        if pd.isna(elevation):
            elevation = None
        locality.elevation = elevation
        locality.georeference_protocol = data['georef_protocol']
        locality.locality_description = data['Locality Description']
        lat_dd = data['lat_dd']
        lon_dd = data['lon_dd']
        if lat_dd and lon_dd:
            locality.geom = GEOSGeometry("POINT(" + str(lon_dd) + " " + str(lat_dd) + ")", 4326)
        locality.save()
        row_index += 1
    locs_arch = Locality.objects.filter(archaeological_evidence__contains='No')
    locs_arch.update(archaeology_present=False)
    locs_bot = Locality.objects.filter(macrobotanical_evidence__contains='None')
    locs_bot.update(macrobotanical_present=False)
    locs_fossils = Locality.objects.filter(uncollected_taxa__isnull=False)
    locs_fossils.update(uncollected_fossils_present=True)


def import_fossils(source_path=fossils_file_path):
    xls = pd.ExcelFile(source_path)
    df = xls.parse(xls.sheet_names[0])
    row_index = 1
    skipped = []
    unmatched_localities = []

    # Write all the data to verbatim fields
    for i in df.index:
        # these three lines below can probably be replaced with a single create command
        new_instance = Fossil()  # create a new instance
        new_instance.verbatim_row_data = df.loc[i].to_json()  # convert row data to json
        new_instance.save()  # save the instance to the DB

    for fossil in Fossil.objects.all():
        data = json.loads(fossil.verbatim_row_data)  # loads json to dictionary
        catalog_number = data['SpecimenDesignation']
        if pd.isna(catalog_number):
            print(f"Skipping row: {row_index}")
            skipped.append(row_index)
        else:
            print(f"Processing id: {fossil.id} row: {row_index}, specimen:  {catalog_number}")
            locality_name = data['Localities::LocalityDesignation']  # get the locality designator string
            locality_obj, created = Locality.objects.get_or_create(locality_id=locality_name)  # look up locality
            if created:
                unmatched_localities.append(locality_name)
            fossil.locality = locality_obj  # assign locality to fossil
            fossil.catalog_number = data['SpecimenDesignation']  # assign catalog_number
            fossil.description = data['Elements Preserved']
            finder = data['Collectors::Display name']
            person_obj, created = Person.objects.get_or_create(name=finder)
            fossil.found_by = person_obj
            recorder = data['Identifiers::Display name']
            recorder_person_obj, created = Person.objects.get_or_create(name=recorder)
            fossil.recorded_by = recorder_person_obj
            in_situ = data['In situ? Y|N']
            if in_situ in ['N', 'n']:
                fossil.in_situ = False
            elif in_situ in ['Y', 'y']:
                fossil.in_situ = True
            else:
                fossil.in_situ = None
            lat_dd = data['lat_dd']
            lon_dd = data['lon_dd']
            if lat_dd and lon_dd:
                geom = GEOSGeometry("POINT(" + str(lon_dd) + " " + str(lat_dd) + ")", 4326)
            fossil.geom = geom
            fossil.elevation = data['Elevation']
            matrix_adhering = data['Sediment or matrix adhering?']
            if matrix_adhering in ['N', 'n']:
                fossil.matrix_adhering = False
            elif matrix_adhering in ['Y', 'y']:
                fossil.matrix_adhering = True
            else:
                fossil.matrix_adhering = None
            fossil.specimen_id = data['SpecimenID']
            fossil.bed = data['Stratigraphic Horizon']
            taxonomic_problem = data['Taxonomic Problem? Y|N']
            if taxonomic_problem in ['N', 'n']:
                fossil.taxonomic_problem = False
            elif taxonomic_problem in ['Y', 'y']:
                fossil.taxonomic_problem = True
            else:
                fossil.taxonomic_problem = None
            fossil.save()
        row_index += 1
    print(f"Done! Skipped rows: {skipped}")
    print(f"Unmatched_localities: {unmatched_localities}")


def import_people():
    """
    Import people after fossils have been imported
    :return:
    """
    fossils = Fossil.objects.all()
    for f in fossils:
        collector = f.verbatim_row_data['']
