# Generated by Django 3.2.18 on 2023-05-30 07:08

from django.db import migrations
from origins.util import citekey_lookup
from collections import Counter
def update_fossil_references1(apps, schema_editor):
    """
    Add references to fossils mentioned in this reference
    :param apps:
    :param schema_editor:
    :return:
    """
    TurkFossil = apps.get_model('origins', 'TurkFossil')
    Publication = apps.get_model('publications', 'Publication')
    List = apps.get_model('publications', 'List')
    tflist = List.objects.get(list='Turkana Fossils')
    p1 = Publication.objects.get(citekey=citekey_lookup['Leakey and Walker, 1985'])
    p2 = Publication.objects.get(citekey=citekey_lookup['Ward et al., 2015'])
    p1.lists.add(tflist)
    p2.lists.add(tflist)
    f = TurkFossil.objects.get(verbatim_reference_description='Leakey and Walker, 1985 ; Ward et al., 2015')
    f.references.add(p1, p2)
    f.save()

def update_fossil_references2(apps, schema_editor):
    """
    Add references to fossils mentioned in this reference
    :param apps:
    :param schema_editor:
    :return:
    """
    TurkFossil = apps.get_model('origins', 'TurkFossil')
    Publication = apps.get_model('publications', 'Publication')
    List = apps.get_model('publications', 'List')
    tflist = List.objects.get(list='Turkana Fossils')
    p1 = Publication.objects.get(citekey=citekey_lookup['Kramer, 1986'])
    p2 = Publication.objects.get(citekey=citekey_lookup['White, 1986'])
    p1.lists.add(tflist)
    p2.lists.add(tflist)
    f = TurkFossil.objects.get(verbatim_reference_description='Kramer, 1986; White, 1986')
    f.references.add(p1, p2)
    f.save()

class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0117_auto_20230530_0551'),
    ]

    operations = [
        migrations.RunPython(update_fossil_references1, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(update_fossil_references2, reverse_code=migrations.RunPython.noop),
    ]
