from django.test import TestCase
from .models import Character


class CharacterMethodTests(TestCase):
    def test_create_character(self):
        characters_starting_count = Character.objects.count()
        Character.objects.create(charname='testchar1',
                                 chartype='UM',
                                 )
        characters_end_count = Character.objects.count()
        self.assertEqual(characters_end_count, characters_starting_count+1)
