from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GEOSGeometry
import json
import projects.utilities as utils
from .models import *
import pandas as pd


# Import file location
file_path = '/Users/dreed/Documents/paleocore/projects/wormil/wormil.xlsx'


def write_row_to_verbatim(df, app_label, model, field_name):
    """

    :param df:
    :param app_label:
    :param model:
    :param field_name:
    :return:
    """
    # Get the model class for the app
    model_class = ContentType.objects.get(app_label=app_label, model=model).model_class()
    # iterate through the DF and convert each row to a dictionary
    for row_dict in df.to_dict('records'):
        row_json = json.dumps(row_dict)
        # these three lines below can probably be replaced with a single create command
        new_instance = model_class()  # create a new instance
        setattr(new_instance, field_name, row_json)  # update the verbatim field with the json data
        new_instance.save()  # save the instance to the DB


def main(source_path=file_path):
    xls = pd.ExcelFile(source_path)
    df = xls.parse(xls.sheet_names[0])

    # Write all the data to verbatim fields
    for row_dict in df.to_dict('records'):
        row_json = json.dumps(row_dict)
        # these three lines below can probably be replaced with a single create command
        new_instance = Fossil()  # create a new instance
        new_instance.verbatim_row_data = row_json
        new_instance.save()  # save the instance to the DB

    for fossil in Fossil.objects.all():
        data = json.loads(fossil.verbatim_row_data)  # loads json to dictionary
        locality_name = data['Localities::LocalityDesignation']  # get the locality designator string
        locality_obj, created = Locality.objects.get_or_create(name=locality_name)  # look up locality
        fossil.locality = locality_obj  # assign locality to fossil
        fossil.catalog_number = data['SpecimenDesignation']  # assign catalog_number
        fossil.description = data['Elements Preserved']
        lat_dd = utils.dms2dd(data['Latitude Degrees'], data['Latitude Minutes'], data['Latitude Seconds'])
        lon_dd = utils.dms2dd(data['Longitude Degrees'], data['Longitude Minutes'], data['Longitude Seconds'])
        geom = GEOSGeometry("POINT(" + str(lon_dd) + " " + str(lat_dd) + ")", 4326)
        fossil.geom = geom
        fossil.elevation = data['Elevation']
        fossil.save()
