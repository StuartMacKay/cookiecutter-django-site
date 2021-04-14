from django.conf import settings
from django.urls import include, path
from django.contrib import admin
{%- if cookiecutter.cms == "wagtail" %}

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name='search'),
]
{% else %}
urlpatterns = [
    path("admin/", admin.site.urls),
]
{%-endif %}

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
{%- if cookiecutter.use_debug_toolbar == "y" or cookiecutter.use_sentry == "" %}

if settings.ENV == "dev" and settings.DEBUG:
{%- if cookiecutter.use_debug_toolbar == "y" %}
    import debug_toolbar
{%- endif %}
{%- if cookiecutter.use_debug_toolbar == "y" %}

    # Add a view that raises and error to test sentry in development
    def trigger_error(request):
        raise Exception("Verify Sentry is configured and working")

    urlpatterns += [path("__debug__/sentry/", trigger_error)]
{%- endif %}
{%- if cookiecutter.use_debug_toolbar == "y" %}
    urlpatterns += [path("__debug__/toolbar/", include(debug_toolbar.urls))]
{%- endif %}

{%- endif %}
{%- if cookiecutter.cms == "wagtail" %}

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]{%- endif %}

