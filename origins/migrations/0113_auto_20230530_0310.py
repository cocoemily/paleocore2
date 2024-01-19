# Generated by Django 3.2.18 on 2023-05-30 03:10

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
        'Leakey, 1970': 'Leakey1970',
        'Wood, 1991': 'Wood1991',
        'Ward et al., 2015': 'Ward2015',
        'Spoor et al., 2007': 'Spoor2007',
        'Walker et al., 1986': 'Walker1986',
        'Howell and Coppens, 1976': 'Howell1976',
        'Daver et al., 2018': 'Daver2018',
        'Leakey and Walker, 1976': 'Leakey1976-lt',
        'Heinrich et al., 1993': 'Heinrich1993',
        'Brown et al., 1993': 'Brown1993-xk',
        'Patterson & Howells, 1967': 'Patterson1967-nw',
        'Lague et al., 2019': 'Lague2019',
        'Patterson et al., 1970': 'Patterson1970',
        'Prat et al., 2005': 'Prat2005-ai',
        'Maddux et al., 2015': 'Maddux2015',
        'Deloison, 1986': 'Deloison1986',
        'Arambourg and Coppens, 1967': 'Arambourg1967',
        'Suwa 1990': 'Suwa1990',
        'Deloison, 1997': 'Deloison1997',
        'Wynn et al., 2020': 'Wynn2020-fc',
        'McHenry, 1994': 'McHenry1994'
    }
    for key in citekey_lookup:
        publication = Publication.objects.get(citekey=citekey_lookup[key])
        publication.lists.add(tflist)
        for f in TurkFossil.objects.filter(verbatim_reference_first_mention=key):
            f.references.add(publication)
            f.save()
class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0112_auto_20230530_0231'),
    ]

    operations = [
        migrations.RunPython(update_fossil_references, reverse_code=migrations.RunPython.noop),
    ]