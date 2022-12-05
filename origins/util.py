import unicodecsv
from origins.models import *
from difflib import SequenceMatcher
from lxml import etree
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
from django.utils.text import slugify
import pandas
import re
from wagtail.core.models import Page
from origins.models.fossil import TurkFossil
# import shapefile

# pbdb_file_path = "/Users/reedd/Documents/projects/ete/pbdb/pbdb_test_no_header.csv"
pbdb_collections_contexts_file_path = "/Users/reedd/Documents/projects/ete/pbdb/pbdb_collections_Africa_no_header.csv"

# pbdb_refs_path = "/Users/reedd/Documents/projects/ete/pbdb/pbdb_refs_test.csv"
pbdb_collection_refs_path = "/Users/reedd/Documents/projects/ete/pbdb/pbdb_refs_colls.csv"
pbdb_occurrence_refs_path = "/Users/reedd/Documents/projects/ete/pbdb/pbdb_refs_occurs.csv"

# si_ho_path = "/Users/reedd/Documents/projects/ete/si_ho/si_ho_specimens_test.xml"
hopdb_path = "/Users/reedd/Documents/projects/ete/si_ho/si_ho_specimens.xml"


def import_pbdb_refs(path):
    with open(path, 'U') as csvfile:
        reader = unicodecsv.DictReader(csvfile, encoding='utf-8')
        count = 0
        created_count = 0
        for row in reader:
            ref_dict = {f: row[f] for f in reader.fieldnames}
            # Check if ref exists using reference_no, if doesn't exist, create a new one.
            obj, created = Reference.objects.get_or_create(reference_no=row['reference_no'],
                                                           defaults=ref_dict)
            obj.source = 'pbdb'
            obj.save()
            if created:
                created_count += 1
            count += 1
        print('Successfully import {} references'.format(count))
        print('Report: {} processed, {} created'.format(count, created_count))


def import_pbdb_collections_to_contexts(path):
    """
    Read data from csv file and create new context objects
    :param path:
    :return:
    """
    csv_file = open(path, 'U')
    reader = unicodecsv.DictReader(csv_file, encoding='utf-8')
    count = 0

    for row in reader:
        new_context = Context()
        for field in reader.fieldnames:
            value = row[field]
            if value in ['', ' ']:
                value = None
            new_context.__setattr__(field, value)
        new_context.geom = "Point({} {})".format(row['lng'], row['lat'])
        new_context.source = "pbdb"
        new_context.save()  # saving here coverts attribute data to proper types
        if new_context.max_ma >= 1.8 and new_context.min_ma <= 7.25:
            new_context.mio_plio = True
        try:
            new_context.reference = Reference.objects.get(reference_no=new_context.reference_no)
        except Reference.DoesNotExist:
            new_context.reference = None
        new_context.save()
        count += 1
    csv_file.close()

    print('Successfully imported {} context objects.'.format(count))
    print('Report: Total: {}, mio_plio: {}'.format(count, Context.objects.filter(mio_plio=True).count()))


def delete_all_contexts():
    contexts = Context.objects.all()
    count = 0
    for c in contexts:
        c.delete()
        count += 1
    print('Successfully deleted all {} Context objects'.format(count))


def delete_all_sites():
    sites = Site.objects.all()
    count = 0
    for c in sites:
        c.delete()
        count += 1
    print('Successfully deleted all {} Site objects'.format(count))


def create_sites_from_contexts():
    """
    Generate the sites by aggregating over the contexts. Contexts are aggregated using the formation field.
    :return:
    """
    contexts = Context.objects.all()
    # create a new site based on first context in each formation
    site_count = 0
    for c in contexts:
        data_dict = {f: c.__getattribute__(f) for f in c.get_concrete_field_names()}
        # Delete dictionary keys unique to context model but not in site model
        context_fields_not_in_site = ['site', 'reference']
        for f in context_fields_not_in_site:
            try:
                del data_dict[f]
            except KeyError:
                pass
        # For each context, c, check if a site exists that has the same formation.
        # If no site exists create a new one using the data from that context.
        obj, created = Site.objects.get_or_create(formation=c.formation, defaults=data_dict)
        if created:
            site_count += 1
        c.site = obj  # assign site fk to each context
        c.save()

    print('Successfully created {} new sites from {} context objects'.format(site_count, contexts.count()))


def create_site_from_context(context):
    """
    Create a new Site from an existing Context
    :param context:
    :return:
    """
    new_site = Site()
    for key in new_site.get_concrete_field_names():
        try:
            new_site.__dict__[key] = context.__dict__[key]
        except KeyError:
            pass
    if new_site.verbatim_lat and new_site.verbatim_lng:
        new_site.geom = Point(float(new_site.verbatim_lng), float(new_site.verbatim_lat))
    new_site.save()

    # context_data_dict = {f: context.__getattribute__(f) for f in context.get_concrete_field_names()}
    # sites_data_dict = {}
    #
    # context_fields_not_in_site = ['site', 'reference']
    # for f in context_fields_not_in_site:
    #     try:
    #         del data_dict[f]
    #     except KeyError:
    #         pass
    # obj, created = Site.objects.get_or_create(name=context.name, defaults=data_dict)
    # if not created:
    #     print("Site {} {} already exists").format(context.id, context.name)
    # else:
    #     context.site = obj
    #     context.save()


def validate_context_references():
    # Validate referential integrity of all context references
    # returns True, []  if all contexts have a reference
    # returns False, [context_id_list] if any contexts are missing references

    result = True
    result_list = []
    for c in Context.objects.all():
        try:
            c.reference = Reference.objects.get(reference_no=c.reference_no)
        except Reference.DoesNotExist:
            result = False
            result_list.append(c.id)
    return result, result_list


def get_tag_list(element_tree):
    """
    Function to generate a list of all element tags from an xml file
    :param element_tree:
    :return:
    """
    return list(set([c.tag for c in element_tree.iter()]))


def import_hopdb_fossil_elements(path):
    """
    Function to import fossil elements from xml file downloaded from the HOP DB.
    This function populates both the FossilElement table and the Fossils table.
    Fossils are aggregated from elements based on values in the HomininElement field
    :param path:
    :return:
    """
    xml_file = open(path, 'U')
    tree = etree.parse(xml_file)  # tree is an lxml ElementTree object
    element_tree = tree.getroot()
    xml_file.close()

    africa_list = [u'Chad', u'Libya', u'South Africa', u'Tanzania', u'Morocco', u'Malawi', u'Ethiopia', u'Algeria',
                   u'Namibia', u'Kenya', u'Zambia']
    asia_list = [u'Israel', u'Indonesia', u'China', u'Vietnam', u'Iraq']
    item_count = 0
    for specimen in element_tree:
        new_fossil_element = FossilElement()
        # specimen_name = specimen.find('HomininElement').text
        specimen_dict = {e.tag: e.text for e in specimen}
        for element in specimen:
            new_fossil_element.__setattr__(element.tag, element.text)
        new_fossil_element.save()
        # try:
        #     print 'created new specimen {} {}'.format(new_fossil_element.id, specimen_name)
        # except UnicodeEncodeError:
        #     print 'created new specimen {}'.format(new_fossil_element.id)
        item_count += 1
        obj, created = Fossil.objects.get_or_create(HomininElement=new_fossil_element.HomininElement,
                                                    defaults=specimen_dict)
        if created:
            if obj.Country:
                if obj.Country in africa_list:
                    obj.continent = 'Africa'
                elif obj.Country in asia_list:
                    obj.continent = 'Asia'
            obj.save()
        new_fossil_element.fossil = obj
    print('Successfully imported {} fossil elements from the HOPDB'.format(item_count))


def get_max_text_lengths(element_tree):
    """
    Function to calculate the maximum length of all text entries in the xml file. This is useful
    for setting the max_length parameters  and correct field types in the model.
    :param element_tree:
    :return: Returns a dict with tag names and max length of text for each tag.
    """
    tag_dict = {}
    for sp in element_tree:
        for element in sp:
            if element.text is not None:
                text_length = len(element.text)
                try:
                    if text_length > tag_dict[element.tag]:
                        tag_dict[element.tag] = text_length
                except KeyError:
                    tag_dict[element.tag] = text_length
    return tag_dict


def get_fossil_placenames():
    """
    Function to fetch a list of unique placenames/contexts for each fossil using the placename field
    :return:
    """
    result_list = []
    unique_placenames = list(set([f.PlaceName for f in Fossil.objects.filter(continent='Africa')]))
    for p in unique_placenames:
        result_list.append([p, Fossil.objects.filter(PlaceName=p).count()])
    return sorted(result_list, key=lambda x: x[1], reverse=True)  # sort list by fossil count descending


def similar(t):
    a, b = t
    return SequenceMatcher(None, a, b).ratio()


def main():
    import_pbdb_refs(path=pbdb_collection_refs_path)
    import_pbdb_refs(path=pbdb_occurrence_refs_path)

    import_pbdb_collections_to_contexts(path=pbdb_collections_contexts_file_path)
    create_sites_from_contexts()

    import_hopdb_fossil_elements(path=hopdb_path)


def get_country_from_geom(geom):
    try:
        country_object = WorldBorder.objects.get(mpoly__intersects=geom)
        country_code = country_object.iso2
    except ObjectDoesNotExist:
        country_code = None
    return country_code


mpath = '/Users/reedd/Documents/projects/origins/makapansgat/makapansgat_hominins.txt'


def import_makapansgat(path=mpath):
    """
    Procudure to import fossil specimen data from Makapansgat
    :param path:
    :return:
    """
    data_file = open(path, 'U')
    lines = data_file.readlines()
    # header = lines[0]
    # site = Site.objects.get(pk=6251)  # get Makapansgat site
    for line in lines[1:]:  # iterate through lines in the data file
        data = line.split('\t')  # tab delimited
        new_fossil = Fossil(catalog_number=data[0])  # create a new fossil
        new_fossil.description = data[1]
        new_fossil.verbatim_PlaceName = data[2]
        specimen_string = 'cat_no: {}  element: {}  place: {}'.format(new_fossil.catalog_number, new_fossil.description,
                                                                      new_fossil.verbatim_PlaceName)
        print(specimen_string)
        new_fossil.save()


gs_path = '/Users/reedd/Documents/projects/origins/gw_hod/human_origins_db_all_records.txt'


def import_gwhod(path=gs_path):
    """
    Procedure to read in data from the George Washington University Human Origins Database
    :param path:
    :return:
    """
    data_file = open(path, 'U')
    lines = data_file.readlines()
    data_file.close()
    for line in lines[410:]:  # skip header
        data = line.split('\t')
        catalog_number = data[0].strip()  # remove extra whitespace
        taxon_name = data[1].strip()
        try:
            Fossil.objects.get(catalog_number=catalog_number)
        except Fossil.DoesNotExist:
            if taxon_name not in ['Homo erectus']:
                print(line)

# def export_sites2shape(filepath='/Users/reedd/Desktop/sites'):
#     """
#     Export a dataset to shapefile format
#     :param geo_obj:
#     :param export_filepath:
#     :return:
#     """
#     w = shapefile.Writer(shapeType=1)
#     osites = Site.objects.filter(origins=True)
#     w.field('Name', 'C')
#     w.field('Formation', 'C')
#     w.field('Occurs', 'N')
#     w.field('Max_ma', 'N', decimal=2)
#     w.field('Min_ma', 'N', decimal=2)
#
#     for s in osites:
#         w.point(s.geom.x, s.geom.y)
#         w.record(s.name, s.formation, s.fossil_count, s.max_ma, s.min_ma)
#     w.save(filepath)


def create_site_page(site_obj):
    """
    Procedure to create a new Origins.SitePage related to a Site object using a template. The template is used
    to provide default entries and to set the position in the page hierarchy.
    :return:
    """
    # This is clunky and assumes a page titled "Template" exists.
    template_page = Page.objects.get(title='Template')
    site_slug = slugify(site_obj.name)
    update_dict = dict(
        site=site_obj,
        slug=slugify(site_slug),
        title=site_obj.name,
        body=None,
        location=site_obj.geom,
        date=site_obj.date_created,
        feed_image=None,
        intro=site_obj.name
    )
    template_page.copy(update_attrs=update_dict)


def create_fossil_page(fossil_obj):
    template_page = Page.objects.get(title='FossilTemplate')
    fossil_slug = slugify(fossil_obj.catalog_number)
    update_dict = dict(
        fossil=fossil_obj,
        slug=fossil_slug,
        title=fossil_obj.catalog_number,
        body=None,
        location=fossil_obj.geom,
        date=fossil_obj.created,
        feed_image=None,
        intro=fossil_obj.catalog_number
    )
    template_page.copy(update_attrs=update_dict)


def taxon2mptt(taxon_obj):
    """
    Match a Taxon instance to a corresponding MPTTTaxon instance.
    :param taxon_obj:
    :return: MPTTTaxon or None
    """
    try:
        match = TTaxon.objects.get(name=taxon_obj.name)
    except ObjectDoesNotExist:
        match = None
    return match


def ttaxa2nomina():
    ttaxa = TTaxon.objects.all()
    for t in ttaxa:
        n = Nomen()
        n.from_ttaxon(t)


def fossil_taxa():
    fossils = Fossil.objects.all()
    fossil_taxa_list = []
    for f in fossils:
        if f.taxon:
            fossil_taxa_list.append(f.taxon)
    return list(set(fossil_taxa_list))


def update_ttaxon():
    for t in TTaxon.objects.all():
        if t.name and not t.epithet:
            t.epithet = t.name
        t.name = t.label
        t.save()


# Utility functions for processing Marchal Turkana Data
def clean_catno(catno):
    """
    Remove leading zeros from catalog numbers
    :param catno:
    :return:
    """
    res = None
    try:
        cc, cn = catno.split(' ')
        res = ' '.join([cc, cn.lstrip('0')])
    except ValueError:
        res = catno
    return res


def import_turkana_fossils(file='origins/data/turkana_inventory.xlsx'):
    """
    Preliminary helper function to quickly read in basic turkana homiinin fossil data from spreadsheets
    :param file:
    :return:
    """
    pd = pandas
    xleast = pd.read_excel(file, sheet_name='East')
    xleast.name = 'east'
    xlwest = pd.read_excel(file, sheet_name='West')
    xlwest.name = 'west'
    xlnorth = pd.read_excel(file, sheet_name='North')
    xlnorth.name = 'north'
    sheets = [xleast, xlwest, xlnorth]
    for sheet in sheets:
        for row in sheet.itertuples(index=False):
            TurkFossil.objects.create(verbatim_catalog_number=row[0], verbatim_suffix=row[1], region=sheet.name)


def import_turk_fossils(file='origins/data/turkana_inventory.xlsx'):
    """
    Import hominin fossil data from an xl spreadsheet.
    :param file:
    :return:
    """
    pd = pandas
    data = pd.read_excel(file)
    for index, row in data.iterrows():
        data_dictionary = {
            'verbatim_inventory_number': row['inventory'],
            'verbatim_suffix': row['suffix'],
            'verbatim_year_discovered': row['discovered'],
            'verbatim_year_mentioned': row['mentioned'],
            'verbatim_year_published': row['published'],
            'verbatim_country': row['country'],
            'verbatim_zone': row['zone'],
            'verbatim_area': row['area'],
            'verbatim_locality': row['locality'],
            'verbatim_formation': row['formation'],
            'verbatim_member': row['member'],
            'verbatim_level': row['level'],
            'verbatim_age_g1': row['age_g1'],
            'verbatim_age_g2': row['age_g2'],
            'verbatim_anatomical_part': row['part'],
            'verbatim_anatomical_description': row['description'],
            'verbatim_taxonomy1': row['taxonomy1'],
            'verbatim_taxonomy2': row['taxonomy2'],
            'verbatim_robusticity': row['rubusticity'],
            'verbatim_finder': row['finder'],
            'verbatim_reference_first_mention': row['ref_first_mention'],
            'verbatim_reference_description': row['ref_description'],
            'verbatim_reference_identification': row['ref_identification'],
            'verbatim_reference_dating': row['ref_dating'],
            'region': row['region'],
            'catalog_number': row['catalog_number'],
            'suffix_assigned': row['suffix_assigned'],
        }
        tf = TurkFossil.objects.create(**data_dictionary)
        tf.save()


def match_catalog_numbers(file='origins/data/turkana_cat2.xlsx'):
    matched = []
    unmatched = []
    pd = pandas
    xl = pd.read_excel(file, sheet_name='East')
    catno = xl['Catno']
    cleaned = [clean_catno(c) for c in catno]

    east_turkana_site = Site.objects.get(name='East Turkana')
    origins_list = Fossil.objects.filter(site=east_turkana_site)
    for c in cleaned:  # iterate through each catalog number in FMSP dataset
        p = re.compile(c)  # compile
        for f in origins_list:
            m = p.match(f.catalog_number)  # attempt to match the FMSP catno to origins
            if m:  # if there's a match append to matched list
                matched.append(c)
            else:
                unmatched.append(c)
    return matched, unmatched


def get_marchal(origins_fossil_obj):
    """
    Get a qs of Marchal fossil objects matching an origins object
    :param origins_fossil_obj:
    :return: queryset of Marchal fossils matching origins fossil
    """
    f = origins_fossil_obj
    catno = f.catalog_number.upper()
    matched = TurkFossil.objects.filter(catalog_number__startswith=catno)
    if not matched:
        catno = f.catalog_number
        matched = TurkFossil.objects.filter(catalog_number__startswith=catno)
    return matched


def get_origins(marchal_fossil_obj):
    """
    Get a qs of Origins fossil objects matching a Marchal TurkanaFossil object
    :param marchal_fossil_obj:
    :return: Return a qs of matching Origins Fossil objects
    """
    f = marchal_fossil_obj
    # catno = f.catalog_number.upper()
    matched = Fossil.objects.filter(catalog_number__startswith=f.catalog_number)
    return matched


def catalog_number_from_verbatim(fossil_obj):
    """
    Format a full catalog number from verbatim catalog number and suffix and write to catalog_number field
    :param fossil_obj:
    """
    if fossil_obj.region == 'east':
        catno = clean_catno(fossil_obj.verbatim_catalog_number)
        if fossil_obj.verbatim_suffix != '##':
            full_catno = catno + '-' + fossil_obj.verbatim_suffix.upper()
        else:
            full_catno = catno
        fossil_obj.catalog_number = full_catno
        fossil_obj.save()


def update_catalog_nubmers():
    """
    Update all catalog_number entries for East Turkna
    :return:
    """
    etfs = TurkFossil.objects.filter(region='east')
    for f in etfs:
        catalog_number_from_verbatim(f)


def origins_in_marchal(sites=['east']):
    """
    For all fossils in origins find matches in Marchal
    :return:
    """
    matched = []
    unmatched = []
    et = Site.objects.get(name='East Turkana')
    fj = Site.objects.get(name='Fejej')
    kp = Site.objects.get(name='Kanapoi')
    wt = Site.objects.get(name='West Turkana')
    om = Site.objects.get(name='Omo Shungura')
    site_object_list = []
    origins_fossils = []

    if 'east' in sites:
        site_object_list.append(fj)
        site_object_list.append(et)
    if 'west' in sites:
        site_object_list.append(wt)
        site_object_list.append(kp)
    if 'north' in sites:
        site_object_list.append(om)

    for site_obj in site_object_list:
        origins_fossils = origins_fossils + list(Fossil.objects.filter(site=site_obj).order_by('catalog_number'))
    for fossil_obj in origins_fossils:
        m = get_marchal(fossil_obj)
        if m:
            matched.append(fossil_obj)
        else:
            unmatched.append(fossil_obj)
    return matched, unmatched


def marchal_in_origins(regions=['east']):
    """
    Get lists of matched and unmatched fossil objects from origins.fossils
    :param regions:
    :return:
    """
    matched = []
    unmatched = []
    for region in regions:
        marchal_fossils = TurkFossil.objects.filter(region__in=regions).order_by('catalog_number')
    for fossil_obj in marchal_fossils:
        m = get_origins(fossil_obj)
        if m:
            matched.append(fossil_obj)
        else:
            unmatched.append(fossil_obj)
    return matched, unmatched


def update_turkana_fossils_in_origins(regions=['east']):
    matched_fossils, unmatched_fossils = marchal_in_origins(regions)
    for fossil in unmatched_fossils:
        fossil.in_origins=False
        fossil.save()
    for fossil in matched_fossils:
        fossil.in_origins=True
        fossil.save()


def update_in_origins():
    """
    Helper function to update the in_origins field in TurkFossil
    :return:
    """
    for f in TurkFossil.objects.all():
        m = get_origins(f)
        if len(m) == 2:
            f.in_origins = True
            f.save()


def update_nomen_genus_species():
    nomina = Nomen.objects.all()
    species_rank = TaxonRank.objects.get(name="Species")
    genus_rank = TaxonRank.objects.get(name="Genus")
    family_rank = TaxonRank.objects.get(name="Family")
    for n in nomina:
        if n.taxon_rank_obj == species_rank:
            try:
                name_list = n.name.split(" ")
                n.generic_name = name_list[0]
                n.specific_epithet = name_list[1]
                n.taxon_rank_group = 'species-group'
            except IndexError:
                n.specific_epithet = n.name
        elif n.taxon_rank_obj == genus_rank:
            n.generic_name = n.name
            n.taxon_rank_group = 'genus-group'
        elif n.taxon_rank_obj == family_rank:
            n.taxon_rank_group = 'family-group'
        n.save()


def add_fossil():
    turk2add = []
    et = Site.objects.get(name='East Turkana')
    for f in turk2add:
        Fossil.objects.create(catalog_number=f.catalog_number, site=wt, country='KE', continent='Africa', origins=True)

