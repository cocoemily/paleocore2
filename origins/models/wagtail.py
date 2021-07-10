# Origins Wagtail models
from django.contrib.gis.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel,
    StreamFieldPanel)
from wagtail.search import index
from utils.models import RelatedLink, CarouselItem

from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtailgeowidget.edit_handlers import GeoPanel
import origins.models

# Wagtail models to move to separate directory
# Origins Wagtail models

class SiteIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('SiteIndexPage', related_name='related_links')


class SiteIndexPage(Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    @property
    def get_sites_pages(self):
        # Get list of live site pages that are descendants of this page
        site_page_list = SitePage.objects.live().descendant_of(self)

        # Order by most recent date first
        site_page_list = site_page_list.order_by('title')

        return site_page_list

    def get_context(self, request):
        # Get site_list
        site_page_list = self.get_sites_pages

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            site_page_list = site_page_list.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(site_page_list, 50)  # Show 50 site_list per page
        try:
            site_page_list = paginator.page(page)
        except PageNotAnInteger:
            site_page_list = paginator.page(1)
        except EmptyPage:
            site_page_list = paginator.page(paginator.num_pages)

        # Update template context
        context = super(SiteIndexPage, self).get_context(request)
        context['site_pages'] = site_page_list
        return context


SiteIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('related_links', label="Related links"),
]

SiteIndexPage.promote_panels = Page.promote_panels


class SitePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('SitePage', related_name='carousel_items')


class SitePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('SitePage', related_name='related_links')


class SitePageTag(TaggedItemBase):
    content_object = ParentalKey('SitePage', related_name='tagged_items')


class SitePage(Page):
    site = models.ForeignKey('Site', null=True, blank=True, on_delete=models.SET_NULL)
    intro = RichTextField()
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    tags = ClusterTaggableManager(through=SitePageTag, blank=True)
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    location = models.PointField(srid=4326, null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
    is_public = models.BooleanField(default=False)


    @property
    def get_taxa(self):
        """
        This function requires a bit more work because at present Fossils are not linked to taxa!
        :return:
        """
        fossils = self.get_fossils

    def get_context(self, request):
        """
        Add fossils to the site context
        :param request:
        :return:
        """
        # Get site_list
        fossil_list = self.get_fossils

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            fossil_list = fossil_list.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(fossil_list, 10)  # Show 10 site_list per page
        try:
            site_list = paginator.page(page)
        except PageNotAnInteger:
            site_list = paginator.page(1)
        except EmptyPage:
            site_list = paginator.page(paginator.num_pages)

        # Update template context
        context = super(SitePage, self).get_context(request)
        context['fossil_list'] = fossil_list
        return context

    @property
    def site_index(self):
        # Find closest ancestor which is a site index
        return self.get_ancestors().type(SiteIndexPage).last()


SitePage.content_panels = [
    FieldPanel('site'),
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('body'),
    InlinePanel('carousel_items', label="Carousel items"),
    InlinePanel('related_links', label="Related links"),
    GeoPanel('location')
]

SitePage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
]


class OriginsSiteIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('OriginsSiteIndexPage', related_name='related_links')


class OriginsSiteIndexPage(Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    @property
    def get_sites_pages(self):
        # Get list of live site pages that are descendants of this page
        site_page_list = OriginsSitePage.objects.live().descendant_of(self)

        # Order by most recent date first
        site_page_list = site_page_list.order_by('title')

        return site_page_list

    def get_context(self, request):
        # Get site_list
        site_page_list = self.get_sites_pages

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            site_page_list = site_page_list.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(site_page_list, 50)  # Show 50 site_list per page
        try:
            site_page_list = paginator.page(page)
        except PageNotAnInteger:
            site_page_list = paginator.page(1)
        except EmptyPage:
            site_page_list = paginator.page(paginator.num_pages)

        # Update template context
        context = super(OriginsSiteIndexPage, self).get_context(request)
        context['site_pages'] = site_page_list
        return context


OriginsSiteIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('related_links', label="Related links"),
]

OriginsSiteIndexPage.promote_panels = Page.promote_panels


class OriginsSitePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('OriginsSitePage', related_name='carousel_items')


class OriginsSitePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('OriginsSitePage', related_name='related_links')


class OriginsSitePageTag(TaggedItemBase):
    content_object = ParentalKey('OriginsSitePage', related_name='tagged_items')


class OriginsSitePage(Page):
    site = models.ForeignKey('Site', null=True, blank=True, on_delete=models.SET_NULL)
    intro = RichTextField()
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    tags = ClusterTaggableManager(through=OriginsSitePageTag, blank=True)
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    location = models.PointField(srid=4326, null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
    is_public = models.BooleanField(default=False)


    @property
    def get_taxa(self):
        """
        This function requires a bit more work because at present Fossils are not linked to taxa!
        :return:
        """
        fossils = self.get_fossils

    def get_context(self, request):
        """
        Add fossils to the site context
        :param request:
        :return:
        """
        # Get site_list
        fossil_list = self.get_fossils

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            fossil_list = fossil_list.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(fossil_list, 10)  # Show 10 site_list per page
        try:
            site_list = paginator.page(page)
        except PageNotAnInteger:
            site_list = paginator.page(1)
        except EmptyPage:
            site_list = paginator.page(paginator.num_pages)

        # Update template context
        context = super(OriginsSitePage, self).get_context(request)
        context['fossil_list'] = fossil_list
        return context

    @property
    def site_index(self):
        # Find closest ancestor which is a site index
        return self.get_ancestors().type(OriginsSiteIndexPage).last()


OriginsSitePage.content_panels = [
    FieldPanel('site'),
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('body'),
    InlinePanel('carousel_items', label="Carousel items"),
    InlinePanel('related_links', label="Related links"),
    GeoPanel('location')
]

OriginsSitePage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
]
#
#
# class OriginsFossilIndexPageRelatedLink(Orderable, RelatedLink):
#     page = ParentalKey('OriginsFossilIndexPage', related_name='fossil_related_links')
#
#
# class OriginsFossilIndexPage(Page):
#     intro = RichTextField(blank=True)
#
#     search_fields = Page.search_fields + [
#         index.SearchField('intro'),
#     ]
#
#     @property
#     def get_child_pages(self):
#         # Get list of live site pages that are descendants of this page
#         fossil_page_list = OriginsFossilPage.objects.live().descendant_of(self)
#
#         # Order by most recent date first
#         fossil_page_list = fossil_page_list.order_by('title')
#
#         return fossil_page_list
#
#     def get_context(self, request):
#         # Get site_list
#         fossil_page_list = self.get_child_pages
#
#         # Filter by tag
#         tag = request.GET.get('tag')
#         if tag:
#             fossil_page_list = fossil_page_list.filter(tags__name=tag)
#
#         # Pagination
#         page = request.GET.get('page')
#         paginator = Paginator(fossil_page_list, 50)  # Show 50 site_list per page
#         try:
#             fossil_page_list = paginator.page(page)
#         except PageNotAnInteger:
#             fossil_page_list = paginator.page(1)
#         except EmptyPage:
#             fossil_page_list = paginator.page(paginator.num_pages)
#
#         # Update template context
#         context = super(OriginsFossilIndexPage, self).get_context(request)
#         context['site_pages'] = fossil_page_list
#         return context
#
#
# OriginsFossilIndexPage.content_panels = [
#     FieldPanel('title', classname="full title"),
#     FieldPanel('intro', classname="full"),
#     InlinePanel('fossil_related_links', label="Related links"),
# ]
#
# OriginsFossilIndexPage.promote_panels = Page.promote_panels
#
#
# class OriginsFossilPageCarouselItem(Orderable, CarouselItem):
#     page = ParentalKey('OriginsFossilPage', related_name='fossil_carousel_items')
#
#
# class OriginsFossilPageRelatedLink(Orderable, RelatedLink):
#     page = ParentalKey('OriginsFossilPage', related_name='fossil_related_links')
#
#
# class OriginsFossilPageTag(TaggedItemBase):
#     content_object = ParentalKey('OriginsFossilPage', related_name='fossil_tagged_items')
#
#
# class OriginsFossilPage(Page):
#     fossil = models.ForeignKey('Fossil', null=True, blank=True, on_delete=models.SET_NULL)
#     intro = RichTextField()
#     body = StreamField([
#         ('heading', blocks.CharBlock(classname="full title")),
#         ('paragraph', blocks.RichTextBlock()),
#         ('image', ImageChooserBlock()),
#     ])
#     tags = ClusterTaggableManager(through=OriginsFossilPageTag, blank=True)
#     date = models.DateField("Post date")
#     feed_image = models.ForeignKey(
#         'wagtail.images.models.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#     location = models.PointField(srid=4326, null=True, blank=True)
#
#     search_fields = Page.search_fields + [
#         index.SearchField('body'),
#     ]
#     is_public = models.BooleanField(default=False)
#
#
#     @property
#     def fossil_index(self):
#         # Find closest ancestor which is a fossil index
#         return self.get_ancestors().type(OriginsFossilIndexPage).last()
#
#
# OriginsFossilPage.content_panels = [
#     FieldPanel('fossil'),
#     FieldPanel('title', classname="full title"),
#     FieldPanel('date'),
#     FieldPanel('intro', classname="full"),
#     StreamFieldPanel('body'),
#     InlinePanel('fossil_carousel_items', label="Carousel items"),
#     InlinePanel('fossil_related_links', label="Related links"),
#     #GeoPanel('location')
# ]
#
# OriginsFossilPage.promote_panels = Page.promote_panels + [
#     ImageChooserPanel('feed_image'),
#     FieldPanel('tags'),
# ]
