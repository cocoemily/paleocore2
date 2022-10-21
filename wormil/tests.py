from django.test import TestCase
from .models import *
from django.contrib.gis.geos import Point
from datetime import datetime


class FossilCreationMethodTests(TestCase):
    """
    Test Fossil instance creation and methods
    """
    def test_fossil_save_simple(self):
        starting_record_count = Fossil.objects.count()  # get current number of fossil records
        new_fossil = Fossil(geom=Point(40.500, 11.526),
                            catalog_number='TST-VP-00')
        new_fossil.save()
        now = datetime.now()
        self.assertEqual(Fossil.objects.count(), starting_record_count+1)  # test that a Fossil was crated.
