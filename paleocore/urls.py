# flake8: noqa
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.images.views.serve import ServeView
from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views

from wagtail_feeds.feeds import (
    BasicFeed, BasicJsonFeed, ExtendedFeed, ExtendedJsonFeed
)

admin.autodiscover()


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', include(wagtailadmin_urls)),
    path('search/', search_views.search, name='search'),
    path('documents/', include(wagtaildocs_urls)),

    # Paleo Core Projects
    path('projects/', include(('projects.urls', 'projects'), namespace='projects')),

    # Feeds
    url('^sitemap.xml$', sitemap),
    url(r'^blog/feed/basic$', BasicFeed(), name='basic_feed'),
    url(r'^blog/feed/extended$', ExtendedFeed(), name='extended_feed'),

    # JSON feed
    url(r'^blog/feed/basic.json$', BasicJsonFeed(), name='basic_json_feed'),
    url(r'^blog/feed/extended.json$', ExtendedJsonFeed(), name='extended_json_feed'),

    url(
        r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$',
        ServeView.as_view(), name='wagtailimages_serve'
    ),

]

# Add urls for the following apps if they are installed
if 'publications' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('publications/', include(('publications.urls', 'publications'), namespace='publications')),
    ]

if 'origins' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('origins/', include(('origins.urls', 'origins'), namespace='origins')),
    ]

if 'paleosites' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('paleosites/', include(('paleosites.urls', 'paleosites'), namespace="paleosites")),
    ]

# For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism. This should be the last item in the urlpatterns list.
urlpatterns += [
    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic.base import RedirectView

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^favicon\.ico$',
            RedirectView.as_view(
                url=settings.STATIC_URL + 'favicon.ico', permanent=True)
            ),
    ]

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
