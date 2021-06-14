from django.test import TestCase
import origins.ontologies as ontologies
from .models import *


######################################
# Tests for models and their methods #
######################################


class OriginsOntologiesTests(TestCase):
    """
    Test origins ontologies
    """

    def test_origins_continent_choices(self):
        """
        Test that the integrity of continent ontology
        """
        self.assertEqual(ontologies.africa, 'Africa')  # test Africa variable
        self.assertEqual(len(ontologies.CONTINENT_CHOICES), 7)  # test there are 7 continents

    def test_origins_choices2list(self):
        """
        Test choices2list method
        :return:
        """
        self.assertEqual(len(ontologies.choices2list(ontologies.CONTINENT_CHOICES)), 7)
        self.assertEqual(ontologies.choices2list(ontologies.CONTINENT_CHOICES)[0], 'Africa')
        self.assertEqual(type(ontologies.choices2list(ontologies.CONTINENT_CHOICES)), list)


class OriginsNominaTests(TestCase):
    """
    Test origins Nomina class
    """

    # Load test data for Taxon, TTaxon, Publications
    fixtures = [
        'origins/fixtures/ttaxon_data_210604.json',
        'origins/fixtures/origins_taxon_data.json',
        'origins/fixtures/publications_testdata.json'
    ]

    def test_nomina_create(self):
        nomina_start_count = Nomen.objects.all().count()
        n = Nomen()
        n.name = 'Australopithecus afarensis'
        n.save()
        nomina_end_count = Nomen.objects.all().count()
        self.assertEqual(nomina_end_count, nomina_start_count + 1)

    def test_from_ttaxon_method(self):
        nomina_start = Nomen.objects.all().count()
        aat = TTaxon.objects.get(name='Australopithecus afarensis')
        n = Nomen()
        n.from_ttaxon(aat)
        self.assertEqual(Nomen.objects.all().count(), nomina_start + 1)
        self.assertEqual(n.name, aat.name)
        self.assertEqual(n.year, aat.year)
        self.assertEqual(n.references.all().count(), aat.references.all().count())

    def test_full_name_metod(self):
        n = Nomen.objects.create(name='Homo sapiens')
        self.assertEqual(n.full_name_html(), '<i>Homo sapiens</i>')
        n.authorship = 'Linnaeus, 1758'
        n.save()
        self.assertEqual(n.full_name_html(), '<i>Homo sapiens</i> Linnaeus, 1758')
        n.name=''
        n.save()
        self.assertEqual(n.full_name_html(), '')

    def test_string_method(self):
        n = Nomen.objects.create(name='Australopithecus africanus')
        self.assertEqual(n.__str__(), f'[{n.id}] Australopithecus africanus')

