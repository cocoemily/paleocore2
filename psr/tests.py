from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.core.files.uploadedfile import TemporaryUploadedFile

import pytz

from psr.views import *
from psr.utilities import *


# Create your tests here.


class ImportShapefileMethodsTest(TestCase):
    fixtures = [
        'psr/fixtures/psr-testing-data.json'
    ]

    def setUp(self):
        self.factory = RequestFactory()
        self.import_shapefile = ImportShapefileDirectory
        self.test_file_path = 'psr/testing-data/PSR Testing_Cave_Rockshelter.zip'
        infile = open(self.test_file_path, 'rb')
        request = self.factory.post('/django-admin/psr/geologicalcontext/import_data/', {'shapefileUpload': infile})
        self.import_shapefile.request = request

    def setup_request(self, request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['some'] = 'some'
        request.session.save()

    def test_get_import_files(self):
        self.assertEqual(self.import_shapefile.get_shp_file(),
                         'psr/testing-data/PSR Testing_Cave_Rockshelter/PSR Testing_Cave_Rockshelter.shp')
        self.assertEqual(self.import_shapefile.get_dbf_file(),
                         'psr/testing-data/PSR Testing_Cave_Rockshelter/PSR Testing_Cave_Rockshelter.dbf')
        self.assertEqual(type(self.import_shapefile.get_shp_file()), TemporaryUploadedFile)
        self.assertEqual(type(self.import_shapefile.get_dbf_file()), TemporaryUploadedFile)

    def test_import_shapefile_directory(self):
        starting_record_count = GeologicalContext.objects.count()  # No geo contexts in empty db
        self.assertEqual(starting_record_count, 0)

        self.setup_request(self.import_shapfile.request)  # annotate the request with a message
        self.import_shapefile.import_shapefile_data()
        self.assertEqual(GeologicalContext.objects.count(), 1)


class ImportJsonMethodsTest(TestCase):
    fixtures = [
        'psr/fixtures/psr-testing-data.json'
    ]

    def setUp(self):
        self.factory = RequestFactory()
        self.import_json = ImportJSON
        self.test_file_path = 'psr/testing-data/test-google-maps-import.json'
        infile = open(self.test_file_path, 'rb')
        request = self.factory.post('/django-admin/psr/geologicalcontext/import_json/', {'jsonUpload': infile})
        self.import_json.request = request

    def setup_request(self, request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['some'] = 'some'
        request.session.save()

    def test_get_import_file(self):
        self.assertEqual(self.import_json.get_import_file().name, self.test_file_path.split('/')[-1])
        self.assertEqual(type(self.import_json.get_import_file()), TemporaryUploadedFile)

    def test_import_json(self):
        starting_record_count = GeologicalContext.objects.count()  # No geo contexts in empty db
        self.assertEqual(starting_record_count, 0)

        self.setup_request(self.import_json.request)  # annotate the request with a message
        self.import_json.import_geo_contexts(self.import_json.get_import_file())
        self.assertEqual(GeologicalContext.objects.count(), 1)


class SurveyOccurrenceMethodsTests(TestCase):
    fixtures = [
        'psr/fixtures/psr-testing-data.json'
    ]

    def test_psr_survey_archaeological_import(self):
        testshp = 'psr/testing-data/PSR Testing_Archaeology/PSR Testing_Archaeology.shp'
        testdbf = 'psr/testing-data/PSR Testing_Archaeology/PSR Testing_Archaeology.dbf'
        testname = "Test lithic 1"

        import_survey_occurrences(testshp, testdbf, [])
        createdOcc = Occurrence.objects.get(name=testname)
        createdArch = Archaeology.objects.get(name=testname)

        now = datetime.now()
        self.assertEqual(createdOcc.date_last_modified.day, now.day)
        self.assertEqual(createdOcc.name, testname)
        self.assertEqual(createdOcc.find_type, "Lithic")
        self.assertEqual(createdOcc.collecting_method, "Exploratory Survey")
        self.assertEqual(createdOcc.item_type, "Archaeological")
        self.assertEqual(createdArch.date_last_modified.day, now.day)
        self.assertEqual(createdArch.archaeology_type, "Lithic")

    def test_psr_survey_biological_import(self):
        testshp = 'psr/testing-data/PSR Testing_Biology/PSR Testing_Biology.shp'
        testdbf = 'psr/testing-data/PSR Testing_Biology/PSR Testing_Biology.dbf'
        testname = "Test Biology 1"

        import_survey_occurrences(testshp, testdbf, [])
        createdOcc = Occurrence.objects.get(name=testname)
        createdBio = Biology.objects.get(name=testname)

        now = datetime.now()
        self.assertEqual(createdOcc.date_last_modified.day, now.day)
        self.assertEqual(createdOcc.name, testname)
        self.assertEqual(createdOcc.find_type, "Microfauna")
        self.assertEqual(createdOcc.collecting_method, "Exploratory Survey")
        self.assertEqual(createdOcc.item_type, "Biological")
        self.assertEqual(createdBio.date_last_modified.day, now.day)
        self.assertEqual(createdBio.archaeology_type, "Microfauna")

    def test_psr_survey_geological_import(self):
        testshp = 'psr/testing-data/PSR Testing_Geology/PSR Testing_Geology.shp'
        testdbf = 'psr/testing-data/PSR Testing_Geology/PSR Testing_Geology.dbf'
        testname = "Test Geo 1"

        import_survey_occurrences(testshp, testdbf, [])
        createdOcc = Occurrence.objects.get(name=testname)
        createdGeo = Geology.objects.get(name=testname)

        now = datetime.now()
        self.assertEqual(createdOcc.date_last_modified.day, now.day)
        self.assertEqual(createdOcc.name, testname)
        self.assertEqual(createdOcc.find_type, "Micromorph")
        self.assertEqual(createdOcc.collecting_method, "Exploratory Survey")
        self.assertEqual(createdOcc.item_type, "Geological")
        self.assertEqual(createdGeo.date_last_modified.day, now.day)
        self.assertEqual(createdGeo.archaeology_type, "Micromorph")

    def test_psr_survey_aggregate_import(self):
        testshp = 'psr/testing-data/PSR Testing_Aggregate/PSR Testing_Aggregate.shp'
        testdbf = 'psr/testing-data/PSR Testing_Aggregate/PSR Testing_Aggregate.dbf'
        testname = "Test Aggregate 1"

        import_survey_occurrences(testshp, testdbf, [])
        createdOcc = Occurrence.objects.get(name=testname)
        createdAgg = Aggregate.objects.get(name=testname)

        now = datetime.now()
        self.assertEqual(createdOcc.date_last_modified.day, now.day)
        self.assertEqual(createdOcc.name, testname)
        self.assertEqual(createdOcc.find_type, "Aggregate")
        self.assertEqual(createdOcc.collecting_method, "Exploratory Survey")
        self.assertEqual(createdOcc.item_type, "Aggregate")
        self.assertEqual(createdAgg.date_last_modified.day, now.day)

    def test_psr_occurrence_save_simple(self):
        starting_record_count = Occurrence.objects.count()  # get current number of occurrence records
        new_occurrence = Occurrence(id=1, item_type="Faunal",
                                    basis_of_record="HumanObservation",
                                    collecting_method="Surface Standard",
                                    field_number=datetime.now(pytz.utc),
                                    geom="POINT (40.8352906016 11.5303732536)")
        new_occurrence.save()
        now = datetime.now()
        self.assertEqual(Occurrence.objects.count(), starting_record_count+1)  # test that one record has been added
        self.assertEqual(new_occurrence.date_last_modified.day, now.day)  # test date last modified is correct
        self.assertEqual(new_occurrence.point_x(), 40.8352906016)
        self.assertEqual(new_occurrence.point_y(), 11.5303732536)

    def test_psr_occurrence_create_method(self):
        starting_record_count = Occurrence.objects.count()
        new_occurrence = Occurrence.objects.create(id=1, item_type="Faunal",
                                                   basis_of_record="HumanObservation",
                                                   collecting_method="Surface Standard",
                                                   field_number=datetime.now(pytz.utc),
                                                   geom="POINT (40.8352906016 11.5303732536)")
        now = datetime.now()
        self.assertEqual(Occurrence.objects.count(), starting_record_count+1)  # test that one record has been added
        self.assertEqual(new_occurrence.date_last_modified.day, now.day)  # test date last modified is correct
        self.assertEqual(new_occurrence.point_x(), 40.8352906016)


class GeologicalContextMethodsTest(TestCase):

    def test_psr_gc_import(self):
        testshp = 'psr/testing-data/PSR Testing_Cave_Rockshelter/PSR Testing_Cave_Rockshelter.shp'
        testdbf = 'psr/testing-data/PSR Testing_Cave_Rockshelter/PSR Testing_Cave_Rockshelter.dbf'
        testname = "Test Cave 1"

        import_geo_contexts(testshp, testdbf, [])
        createdGC = GeologicalContext.objects.get(name=testname)

        now = datetime.now()
        self.assertEqual(createdGC.date_last_modified.day, now.day)
        self.assertEqual(createdGC.name, testname)
        self.assertEqual(createdGC.context_type, "Cave")
        self.assertEqual(createdGC.collecting_method, "Exploratory Survey")

    def test_psr_gc_save_simple(self):
        starting_record_count = GeologicalContext.objects.count()  # get current number of occurrence records
        new_gc = GeologicalContext(id=1, context_type="Cave",
                                    basis_of_record="HumanObservation",
                                    collecting_method="Surface Standard",
                                    field_number=datetime.now(pytz.utc),
                                    geom="POINT (40.8352906016 11.5303732536)")
        new_gc.save()
        now = datetime.now()
        self.assertEqual(GeologicalContext.objects.count(), starting_record_count+1)  # test that one record has been added
        self.assertEqual(new_gc.date_last_modified.day, now.day)  # test date last modified is correct
        self.assertEqual(new_gc.point_x(), 40.8352906016)
        self.assertEqual(new_gc.point_y(), 11.5303732536)

    def test_psr_gc_create_method(self):
        starting_record_count = GeologicalContext.objects.count()
        new_gc = GeologicalContext.objects.create(id=1, context_type="Cave",
                                   basis_of_record="HumanObservation",
                                   collecting_method="Surface Standard",
                                   field_number=datetime.now(pytz.utc),
                                   geom="POINT (40.8352906016 11.5303732536)")
        now = datetime.now()
        self.assertEqual(GeologicalContext.objects.count(), starting_record_count+1)  # test that one record has been added
        self.assertEqual(new_gc.date_last_modified.day, now.day)  # test date last modified is correct
        self.assertEqual(new_gc.point_x(), 40.8352906016)

