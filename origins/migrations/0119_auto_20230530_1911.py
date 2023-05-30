# Generated by Django 3.2.18 on 2023-05-30 19:11

from django.db import migrations

def update_fossil_references(apps, schema_editor):
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
    citekey_lookup = {
        'Howell, 1978': 'Howell1978b',
    }
    for key in citekey_lookup:
        publication = Publication.objects.get(citekey=citekey_lookup[key])
        publication.lists.add(tflist)
        for f in TurkFossil.objects.filter(verbatim_reference_first_mention=key):
            f.references.add(publication)
            f.save()
class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0118_auto_20230530_0708'),
    ]

    operations = [
        migrations.RunPython(update_fossil_references, reverse_code=migrations.RunPython.noop),
    ]
