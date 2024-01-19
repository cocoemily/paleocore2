# Generated by Django 3.2.18 on 2023-05-29 22:40

from django.db import migrations
from collections import Counter

def update_fossils_leakey73a(apps, schema_editor):
    """
    Add Leakey 1973a to fossils mentioned in this reference
    :param apps:
    :param schema_editor:
    :return:
    """
    TurkFossil = apps.get_model('origins', 'TurkFossil')
    Publication = apps.get_model('publications', 'Publication')
    first_pubs = TurkFossil.objects.values_list('verbatim_reference_first_mention', flat=True)
    citekey_lookup = {
        'Leakey et al., 1998': 'Leakey1998',
        'Leakey, 1974': 'Leakey1974-gv',
        'Howell and Coppens, 1974':'Howell1974'
    }

    #leakey98 = Publication.objects.get(citekey='Leakey1998')
    for key in citekey_lookup:
        publication = Publication.objects.get(citekey=citekey_lookup[key])
        for f in TurkFossil.objects.filter(verbatim_reference_first_mention=key):
            f.references.add(publication)
            f.save()

class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0107_auto_20230529_2229'),
    ]

    operations = [
        migrations.RunPython(update_fossils_leakey73a, reverse_code=migrations.RunPython.noop),
    ]