import os
import uuid
# Django imports
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils.html import mark_safe, format_html

# Paleo Core imports
import projects.models
import publications.models
from mptt.models import MPTTModel, TreeForeignKey

from origins.ontologies import NOMENCLATURAL_STATUS_CHOICES, BC_STATUS_CHOICES, NOMENCLATURAL_CODE_CHOICES, \
    TAXON_RANK_GROUP_CHOICES, TYPE_CHOICES, CLASSIFICATION_STATUS_CHOICES, VERIFIER_CHOICES

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from .wagtail import NomenDetailRelatedLink


# Taxonomy models inherited from projects.TaxonRank base project
class TaxonRank(projects.models.TaxonRank):
    """
    A class for Taxonomic Ranks
    Inherits from Paleo Core Base Class
    name
    date_created
    date_last_modified
    problem
    problem_comment
    remarks
    last_import

    Inherits from projects.TaxonRank
    name
    plural
    ordinal
    """
    class Meta:
        verbose_name = "Taxon Rank"
        ordering = ['ordinal']


class Taxon(projects.models.Taxon):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    rank = models.ForeignKey('TaxonRank', null=True, blank=True, on_delete=models.SET_NULL)
    references = models.ManyToManyField(publications.models.Publication, blank=True)

    class Meta:
        verbose_name = "Taxon"
        verbose_name_plural = "Taxa"
        ordering = ['rank__ordinal', 'label']


class IdentificationQualifier(projects.models.IdentificationQualifier):
    class Meta:
        verbose_name = "Identification Qualifier"


class Nomen(projects.models.PaleoCoreBaseClass):
    """
    A class for taxonomic names (nomen).
    The Nomen class inherits the following fields form the PaleoCoreBaseClass:
    name,
    date_created, date_last_modified
    problem, problem_comment
    remarks,
    last_import
    """
    generic_name_help = 'The genus portion of the scientific name, e.g. Homo.'
    specific_epithet_help = 'The trivial (species) portion of the scientific name, e.g. sapiens.'
    authorship_help = 'The authorship of the naming publication, date included, e.g. King, 1864'
    year_help = 'The year the name was published in yyyy format.'
    type_help = 'The catalog number of the type specimen entered as a string, e.g. OH 7'
    type_object_help = 'The type specimen fossil, select from choice list'
    paratypes_help = 'A comma delimited list of catalog number for paratype specimens as given in the source text'

    # scientific_name = self.scientific_name()  self.scientific_name_html()
    # name = models.Charfield ... inherited from parent class. The scientific name without authorship, e.g. Homo sapiens
    scientific_name_id = models.CharField(max_length=255, null=True, blank=True)
    generic_name = models.CharField(max_length=255, null=True, blank=True, help_text=generic_name_help)
    specific_epithet = models.CharField(max_length=255, null=True, blank=True, help_text=specific_epithet_help)
    authorship = models.CharField(max_length=255, null=True, blank=True, help_text=authorship_help)
    year = models.IntegerField('Authorship Year', null=True, blank=True, help_text=year_help)
    authorship_reference_obj = models.ForeignKey(publications.models.Publication, null=True, blank=True,
                                                 on_delete=models.SET_NULL, related_name='name_reference')
    taxon_rank_obj = models.ForeignKey('TaxonRank', null=True, blank=True, on_delete=models.SET_NULL)
    taxon_rank_group = models.CharField(max_length=255, null=True, blank=True,
                                        choices=TAXON_RANK_GROUP_CHOICES, default='species-group')
    nomenclatural_code = models.CharField('Nom. Code', max_length=255, null=True, blank=True,
                                          choices=NOMENCLATURAL_CODE_CHOICES, default='ICZN')
    nomenclatural_status = models.CharField('Nom. Status', max_length=255, null=True, blank=True,
                                            choices=NOMENCLATURAL_STATUS_CHOICES)
    type_specimen_label = models.CharField(max_length=255, null=True, blank=True, help_text=type_help)
    type_specimen = models.ForeignKey('Fossil', null=True, blank=True, on_delete=models.SET_NULL,
                                      help_text=type_object_help)
    paratypes = models.TextField(null=True, blank=True)
    type_taxon = models.CharField(max_length=255, null=True, blank=True)

    bc_status = models.CharField('BC Status', max_length=255, null=True, blank=True,
                                 choices=BC_STATUS_CHOICES)
    is_available = models.BooleanField('Available', default=False)
    is_potentially_valid = models.BooleanField('Pot. Valid', default=False)
    is_objective_synonym = models.BooleanField('Objective Synonym', default=False)
    is_subjective_synonym = models.BooleanField('Subjective Synonym', default=False)
    is_established = models.BooleanField('Established', default=False)

    references = models.ManyToManyField(publications.models.Publication, blank=True)
    assigned_to = models.CharField('Assigned', max_length=255, null=True, blank=True, choices=VERIFIER_CHOICES)
    verified_by = models.CharField('Verified', max_length=255, null=True, blank=True, choices=VERIFIER_CHOICES)
    verified_date = models.DateField(null=True, blank=True)  # used to control visibility on nomen detail page

    def authorship_reference(self):
        """
        Get a basic reference as plain text. Handles articles, books and book chapters.
        :return:
        """
        citation_text = ""
        pub_obj = self.authorship_reference_obj  # publication object
        try:
            authors = pub_obj.authors
            year = pub_obj.year
            article_title = pub_obj.title
            journal_title = pub_obj.journal
            volume = pub_obj.volume
            pages = pub_obj.pages
            book_title = pub_obj.book_title
            publisher = pub_obj.publisher

            # Publication types are:
            # ['Journal', 'Conference', 'Technical Report',
            # 'Book', 'Book Chapter', 'Abstract', 'Thesis', 'Unpublished', 'Patent']
            # Publication bibtex types are:
            # ['article', 'inproceedings', 'techreport', 'book', 'inbook', 'abstract', 'phdthesis', 'unpublished', 'patent']
            if pub_obj.type.type in ['article', 'Journal']:
                citation_text = f'{authors}. {pub_obj.year}. {article_title}. {journal_title}. {volume}: {pages}.'
            elif pub_obj.type.type in ['book', 'Book', 'Thesis']:
                citation_text = f'{authors}. {year}. {book_title}. {publisher}.'
            elif pub_obj.type.type in ['incollection', 'inproceedings', 'inbook', 'Book Chapter']:
                citation_text = f'{authors}. {year}. {article_title} In: {book_title}. {publisher}. pp. {pages}.'
        except AttributeError:
            pass
        return citation_text

    def authorship_reference_id(self):
        """
        Get the unique doi identifier for the reference publication
        :return:
        """
        doi = None
        try:
            doi = self.authorship_reference_obj.doi
        except AttributeError:
            pass
        return doi

    def from_ttaxon(self, ttaxon):
        """
        Create a nomen from a ttaxon instance
        :param ttaxon:
        :return:
        """
        self.name = ttaxon.name
        self.date_created = ttaxon.date_created
        self.date_last_modified = ttaxon.date_last_modified
        self.problem = ttaxon.problem
        self.problem_comment = ttaxon.problem_comment
        self.remarks = ttaxon.remarks
        self.authorship = ttaxon.authorship
        self.year = ttaxon.year
        self.rank = ttaxon.rank
        self.type_specimen = ttaxon.type_specimen
        self.type_status = ttaxon.type_status
        self.paratypes = ttaxon.paratypes
        self.nomenclatural_status = ttaxon.nomenclatural_status
        self.name_reference = ttaxon.name_reference
        self.save()
        self.references.add(*ttaxon.references.all())
        self.save()

    # Note that full scientific names have authorship separated from the genus and species with no punctuation
    # Date is separated from author by a comma. If three or more authors then names can be truncated with et al.
    # See ICZN Article 51.2, Also note that Campbell (1965) does not follow ICZN 4e.
    def scientific_name(self):
        """
        Get the full scientific name with authorship as plain text
        :return:
        """
        scientific_name_string = ''
        if self.name:
            scientific_name_string = self.name
            if self.authorship:
                scientific_name_string += f' {self.authorship}'
        return scientific_name_string

    def full_name_html(self):
        """
        Get the full scientific name formatted as html
        :return:
        """
        full_name_html_string = ''
        if self.name:
            full_name_html_string = f'<i>{self.name}</i>'
            if self.authorship:
                full_name_html_string += f' {self.authorship}'
        return mark_safe(full_name_html_string)

    def scientific_name_html(self):
        """
        alternate named method for full_name_html  to be consistent with scientific name
        :return:
        """
        return self.full_name_html()

    def authorship_year(self):
        return self.year

    def taxon_rank_label(self):
        tr_label = ''
        if self.taxon_rank_obj:
            tr_label = self.taxon_rank_obj.name
        return tr_label

    def type_status(self):
        type_status = None
        try:
            type_status = self.type_specimen.type_status
        except AttributeError:
            pass
        return type_status

    def objective_junior_synonyms(self):
        """
        Get objective junior synonyms associated with this nomen
        :return: Returns None or a queryset of Nomina
        """
        if self.is_objective_synonym:
            result = None
        else:
            try:
                type_obj = self.type_object  # First get the type specimen fossil object assoc. with this nomen
                # from the type get the assoc. nomina that point to it, excluding this name.
                result = type_obj.nomen_set.exclude(pk=self.id)
            except AttributeError:  # if nomen has no type object, raises Attribute error.
                result = None
        return result

    def __str__(self):
        unicode_string = '['+str(self.id)+']'
        if self.name:
            unicode_string = unicode_string+' '+self.scientific_name()
        return unicode_string

    class Meta:
        ordering = ['name']
        verbose_name = 'Nomen'
        verbose_name_plural = 'Nomina'

    # Wagtail
    panels = [FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full title"),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('body'),
    FieldPanel('template_string'),
    InlinePanel('related_links', label="Related links"),]


class ActiveNomen(Nomen):
    class Meta:
        proxy = True
        ordering = ['name']
        verbose_name = 'Active Nomen'
        verbose_name_plural = 'Active Nomina'


class TTaxon(MPTTModel, projects.models.Taxon):
    """
    Modified Preordered Tree Traversal Taxon class
    Inherits name, parent, rank, references from projects.models.Taxon
    """
    verbatim_name = models.CharField(max_length=255, null=True, blank=True)  # name as it appears in 1st publication
    zoobank_id = models.CharField(max_length=255, null=True, blank=True)
    epithet = models.CharField(max_length=255, null=True, blank=True)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)
    authorship = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    type_specimen = models.CharField(max_length=255, null=True, blank=True)
    type_status = models.CharField(max_length=255, null=True, blank=True, choices=TYPE_CHOICES)
    paratypes = models.CharField(max_length=255, null=True, blank=True)
    nomenclatural_code = models.CharField(max_length=255, null=True, blank=True, default='ICZN',
                                          choices=NOMENCLATURAL_CODE_CHOICES)
    bc_status = models.CharField('Nom. Status', max_length=255, null=True, blank=True,
                                            choices=BC_STATUS_CHOICES)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    classification_status = models.CharField('Classif. Status', max_length=255, null=True, blank=True, default='ICZN',
                                          choices=CLASSIFICATION_STATUS_CHOICES)
    junior_to = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='synonyms')
    rank = models.ForeignKey('TaxonRank', null=True, blank=True, on_delete=models.SET_NULL)
    name_reference = models.ForeignKey(publications.models.Publication, null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name='name_references')
    references = models.ManyToManyField(publications.models.Publication, blank=True)

    def _synonyms(self):
        """
        Get list of TTaxa that are synonyms using the junior_to field.
        :return:
        """
        return list(self.synonyms.all())

    def hypodigm(self):
        """
        Get the queryset of Fossil objects that are identified to this taxon
        :return: returns queryset of Fossil objects.
        """
        result = None
        app = self._meta.app_label
        try:
            content_type = ContentType.objects.get(app_label=app, model='fossil')  # assumes the model is named Biology
            this_fossil_model = content_type.model_class()
            result = this_fossil_model.objects.filter(ttaxon=self)
        except ContentType.DoesNotExist:
            pass  # If no matching content type then we'll pass here and return None
        return result

    def fossil_usages(self):
        """
        Count the number of Fossil objects pointing to the ttaxon instance. This method uses
        the content type system to find the containing app and model.
        :return: Returns and integer count of the number of biology instances in the app that point to the taxon.
        """
        return self.hypodigm().count()

    def scientific_name(self):
        """
        Generate pretty format html with full scientific name
        :return:
        """
        scientific_name_html = ''
        name_string = "{otag}{name}{ctag} {auth}".format(otag='<i>' if self.rank.ordinal >= 60 else "",
                                                        name=self.name,
                                                        ctag='</i>' if self.rank.ordinal >= 60 else "",
                                                        auth=self.authorship if self.authorship else "")
        if self.authorship:
            scientific_name_html = '<i>' + self.name + '</i> ' + self.authorship
        else:
            scientific_name_html = '<i>' + self.name + '</i>'
        #return format_html(scientific_name_html)
        return format_html(name_string)

    class Meta:
        verbose_name = "TTaxon"
        verbose_name_plural = "TTaxa"
        ordering = ['rank__ordinal', 'name']

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return str(self.name)
