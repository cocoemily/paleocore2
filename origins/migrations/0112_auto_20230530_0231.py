# Generated by Django 3.2.18 on 2023-05-30 02:31

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
        'Leakey and Walker, 1988': 'Leakey1988-fw',
        'Coffing et al., 1994': 'Coffing1994',
        'Brown et al., 2001': 'Brown2001',
        'Coppens et al., 1973': 'Coppens1973c',
        'Fleagle et al., 1991': 'Fleagle1991',
        'Hammond et al., 2021': 'Hammond2021-tw',
        'Richmond et al., 2020': 'Richmond2020-cz',
        'Leakey and Walker, 2003': 'Leakey2003',
        'Howell, 1968': 'Howell1968-pm',
        'Hunt and Vitzthum, 1986': 'Hunt1986',
        'Prat et al., 2003': 'Prat2003',
        'Boisserie et al., 2008': 'Boisserie2008',
        'Day and Leakey, 1974': 'Day1974',
        'de Lumley and Marchal, 2004': 'Lumley2004',
        'Cerling et al., 2013': 'Cerling2013',
        ' Brown et al., 2001': 'Brown2001',
        'Leakey et al., 2012': 'Leakey2012-nf',
        'Green et al., 2018': 'Green2018-sc',
        'Skinner et al, 2020': 'Skinner2020'
    }
    for key in citekey_lookup:
        publication = Publication.objects.get(citekey=citekey_lookup[key])
        publication.lists.add(tflist)
        for f in TurkFossil.objects.filter(verbatim_reference_first_mention=key):
            f.references.add(publication)
            f.save()

class Migration(migrations.Migration):

    dependencies = [
        ('origins', '0111_auto_20230530_0145'),
    ]

    operations = [
        migrations.RunPython(update_fossil_references, reverse_code=migrations.RunPython.noop),
    ]