from .models import *


def match_taxon(biology_object):
    """
    find taxon objects from item_scientific_name
    Return: (True/False, match_count, match_list)
    """
    # match, match_count, match_list = (False, 0, None)
    match_list = Taxon.objects.filter(name=biology_object.item_scientific_name)
    if len(match_list) == 1:  # one match
        result_tuple = (True, 1, match_list)
    else:
        result_tuple = (False, len(match_list), match_list)
    return result_tuple


def match_element(biology_object):
    """
    find anatomical element from string in item_description. Returns a result tuple. The first element is true
    only if there is one and only one match
    :param biology_object:
    :return: (True/False, match_count, match_list)
    """
    match, match_count, match_list = (False, 0, None)
    element_list = [e[1] for e in HRP_ELEMENT_CHOICES]
    description = biology_object.item_description
    if description.lower() in element_list:
        match = True
        match_count = 1
        match_list = description
    result = (match, match_count, match_list)
    return result


def print_children(t):
    for c in t.get_children():
        print('\t{}'.format(c))


def print_taxon_list():
    mammalia = Taxon.objects.get(name='Mammalia')
    for a in mammalia.get_children():
        print('\t{}\t{}'.format(a, a.biology_usages()))
        for b in a.get_children():
            print('\t\t{}\t{}'.format(b, b.biology_usages()))
            for c in b.get_children():
                print('\t\t\t{}\t{}'.format(c, c.biology_usages()))
                for d in c.get_children():
                    print('\t\t\t\t{}\t{}'.format(d, d.biology_usages()))
                    for e in d.get_children():
                        print('\t\t\t\t\t{}\t{}'.format(e, e.biology_usages()))
                        for f in e.get_children():
                            print('\t\t\t\t\t{}\t{}'.format(f, f.biology_usages()))
                            for g in f.get_children():
                                print('\t\t\t\t\t{}\t{}'.format(g, g.biology_usages()))




    # for t in animalia.get_children():
    #     print(t)
    #     for c in t.get_children():
    #         print('\t{}'.format(c))

    # taxa = Taxon.objects.all()
    # tr = TaxonRank.objects.all()
    # tdict = ()
    # for t in taxa:
    #     if t.biology_usages() > 0:
    #         tdict[t.]
