from django.contrib.gis.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel,
    StreamFieldPanel)
from wagtail.search import index
from utils.models import LinkFields, RelatedLink, CarouselItem
from wagtail.contrib.settings.models import BaseSetting, register_setting
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtailgeowidget.edit_handlers import GeoPanel
from origins.models import *


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL', null=True, blank=True)
    instagram = models.URLField(
        max_length=255, help_text='Your Instagram URL', null=True, blank=True)
    twitter = models.URLField(
        max_length=255, help_text='Your Twitter URL', null=True, blank=True)
    youtube = models.URLField(
        help_text='Your YouTube Channel URL', null=True, blank=True)
    linkedin = models.URLField(
        max_length=255, help_text='Your Linkedin URL', null=True, blank=True)
    github = models.URLField(
        max_length=255, help_text='Your Github URL', null=True, blank=True)
    facebook_appid = models.CharField(
        max_length=255, help_text='Your Facbook AppID', null=True, blank=True)


@register_setting
class SiteBranding(BaseSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    site_name = models.CharField(max_length=250, null=True, blank=True)
    panels = [
        ImageChooserPanel('logo'),
        FieldPanel('site_name'),
    ]


class HomePageContentItem(Orderable, LinkFields):
    page = ParentalKey('pages.HomePage', related_name='content_items')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=100)
    content = RichTextField(null=True, blank=True,)
    summary = RichTextField(blank=True)
    slug = models.SlugField()

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('summary'),
        FieldPanel('content'),
        FieldPanel('slug'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]


class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('pages.HomePage', related_name='carousel_items')


class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.HomePage', related_name='related_links')


class HomePage(Page):
    title_text = RichTextField(null=True, blank=True)
    body = RichTextField(null=True, blank=True)
    feed_image = models.ForeignKey(
        Image,
        help_text="An optional image to represent the page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('body', )

    class Meta:
        verbose_name = "Homepage"


HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('title_text', classname="full"),
    FieldPanel('body', classname="full"),
    InlinePanel('carousel_items', label="Carousel items"),
    InlinePanel('content_items', label="Content Blocks"),
    InlinePanel('related_links', label="Related links"),
]

HomePage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


class StandardIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.StandardIndexPage', related_name='related_links')


class StandardIndexPage(Page):
    TEMPLATE_CHOICES = [
        ('pages/standard_index_page.html', 'Default Template'),
        ('pages/standard_index_page_grid.html', 'Grid Also In This Section'),
    ]
    subtitle = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)
    template_string = models.CharField(
        max_length=255, choices=TEMPLATE_CHOICES,
        default='pages/standard_index_page.html'
    )
    feed_image = models.ForeignKey(
        Image,
        help_text="An optional image to represent the page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('intro', )

    @property
    def template(self):
        return self.template_string


StandardIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full title"),
    FieldPanel('intro', classname="full"),
    FieldPanel('template_string'),
    InlinePanel('related_links', label="Related links"),
]

StandardIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


# Standard page

class StandardPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('pages.StandardPage', related_name='carousel_items')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.StandardPage', related_name='related_links')


class StandardPage(Page):
    TEMPLATE_CHOICES = [
        ('pages/standard_page.html', 'Default Template'),
        ('pages/standard_page_full.html', 'Standard Page Full'),
    ]
    subtitle = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('html', blocks.RawHTMLBlock()),
    ])
    template_string = models.CharField(
        max_length=255, choices=TEMPLATE_CHOICES,
        default='pages/standard_page.html'
    )
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    @property
    def template(self):
        return self.template_string


StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full title"),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('body'),
    FieldPanel('template_string'),
    InlinePanel('carousel_items', label="Carousel items"),
    InlinePanel('related_links', label="Related links"),

]

StandardPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class VideoGalleryPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('pages.VideoGalleryPage', related_name='carousel_items')


class VideoGalleryPage(Page):
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]


VideoGalleryPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('carousel_items', label="Carousel items"),

]

VideoGalleryPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class TestimonialPage(Page):
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]


TestimonialPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
]

TestimonialPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class ContentBlock(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='contentblocks',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255)
    body = RichTextField()
    summary = RichTextField(blank=True)
    slug = models.SlugField()
    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        FieldPanel('summary'),
        FieldPanel('body', classname="full"),
        FieldPanel('slug'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __str__(self):
        return u"{0}[{1}]".format(self.title, self.slug)


register_snippet(ContentBlock)


class Testimonial(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='testimonials',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=150)
    photo = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL
    )
    text = RichTextField(blank=True)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('name'),
        ImageChooserPanel('photo'),
        FieldPanel('text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __str__(self):
        return self.name


register_snippet(Testimonial)


class Advert(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='adverts',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=150, null=True)
    image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL
    )
    button_text = models.CharField(max_length=150, null=True)
    text = RichTextField(blank=True)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('text'),
        FieldPanel('button_text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __str__(self):
        return self.title


register_snippet(Advert)


# Faqs Page

class FaqsPage(Page):
    body = StreamField([
        ('faq_question', blocks.CharBlock(classname="full title")),
        ('faq_answer', blocks.RichTextBlock()),
    ])


FaqsPage.content_panels = [
    FieldPanel('title', classname="full title"),
    StreamFieldPanel('body'),
]


# Origins Wagtail models

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
    site = models.ForeignKey('origins.Site', null=True, blank=True, on_delete=models.SET_NULL)
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
#         'wagtailimages.Image',
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
