from .models import *

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
