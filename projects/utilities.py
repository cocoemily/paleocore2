# Utilities and tools for managing project data
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, FieldError
from django.contrib.gis.geos import Point, Polygon
import xlrd
from datetime import datetime
import pytz
import re
from paleocore.settings import PROJECT_ROOT
import collections
import idigbio
import requests
import string
import pandas as pd
import numpy as np
import json


def open_book(folder, file):
    """
    Open an Excel workbook
    :param folder: string representing folder path with starting and ending slashes,
    e.g. '/Users/dnr266/Documents/PaleoCore/projects/Laetoli/csho_versions/'
    :param file: string representation of the file name, with no slashes, e.g. 'laetoli_csho_1998.xls'
    :return: Returns an xlrd workbook object
    """
    return xlrd.open_workbook(folder+file)


def get_header_list(sheet):
    """
    Get a list of header row cell values.
    :param sheet:
    :return: Returns a list of values from the first row in the sheet.
    """
    return [c.value for c in sheet.row(0)]


def xl2df(excel_file_path):
    """
    Read an excel file and convert it to a Pandas Data Frame
    :param excel_file_path:
    :return:
    """
    xls = pd.ExcelFile(excel_file_path)
    df = xls.parse(xls.sheet_names[0])
    return df


def dms2dd(d, m, s):
    """
    Convert degrees minutes seconds to decimanl degrees
    :param d: degrees
    :param m: minutes
    :param s: seconds
    :return: decimal
    """
    return d+((m+(s/60.0))/60.0)  # divide by 60.0 to insure decimal precision


def extent2poly(extent):
    """
    Convert an extent tuple to a GEOS polygon instance
    :param extent: (minx, miny, maxx, maxy)
    :return:
    """
    minx, miny, maxx, maxy = extent
    return Polygon(((minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)),)

