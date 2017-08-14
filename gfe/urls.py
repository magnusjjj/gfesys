from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

import server.views_normal.SubmissionArchiveDetailOverrideView
from page import views
from surlex.dj import surl
from server import views as server_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'gfe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^forum', include('spirit.urls')),
    url(r'^servers/', include('server.urls', namespace='server')),
	url(r'^groups/', include('gfegroups.urls', namespace='gfegroups', app_name="gfegroups")),
    url(r'^members/', include('member.urls', namespace='member', app_name="member")),
    url(r'^admin/', include(admin.site.urls)),
	surl(
        '^newsletter/<newsletter_slug:s>/archive/<year:Y>/<month:m>/<day:d>/<slug:s>/$',
        server.views_normal.SubmissionArchiveDetailOverrideView.SubmissionArchiveDetailOverrideView.as_view(), name='newsletter_archive_detail_override'
    ),
    url(r'^newsletter/', include('newsletter.urls')),
	
    url(r'^apple-touch-icon-57x57\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-57x57.png', permanent=True)),
    url(r'^apple-touch-icon-60x60\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-60x60.png', permanent=True)),
    url(r'^apple-touch-icon-72x72\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-72x72.png', permanent=True)),
    url(r'^apple-touch-icon-76x76\.png', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-76x76.png', permanent=True)),
    url(r'^apple-touch-icon-114x114\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-114x114.png', permanent=True)),
    url(r'^apple-touch-icon-120x120\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-120x120.png', permanent=True)),
    url(r'^apple-touch-icon-144x144\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-144x144.png', permanent=True)),
    url(r'^apple-touch-icon-152x152\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-152x152.png', permanent=True)),
    url(r'^apple-touch-icon-180x180\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-180x180.png', permanent=True)),
	url(r'^apple-touch-icon-precomposed\.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon-precomposed.png', permanent=True)),
	url(r'^apple-touch-icon.png$', RedirectView.as_view(url='/static/servers/favicons/apple-touch-icon.png', permanent=True)),
    url(r'^favicon-32x32\.png$', RedirectView.as_view(url='/static/servers/favicons/favicon-32x32.png', permanent=True)),
    url(r'^favicon-96x96\.png$', RedirectView.as_view(url='/static/servers/favicons/favicon-96x96.png', permanent=True)),
	url(r'^android-chrome-36x36\.png$', RedirectView.as_view(url='/static/servers/favicons/android-chrome-36x36.png', permanent=True)),
    url(r'^android-chrome-48x48\.png$', RedirectView.as_view(url='/static/servers/favicons/android-chrome-48x48.png', permanent=True)),
	url(r'^android-chrome-72x72\.png$', RedirectView.as_view(url='/static/servers/favicons/android-chrome-72x72.png', permanent=True)),
	url(r'^android-chrome-96x96\.png$', RedirectView.as_view(url='/static/servers/favicons/android-chrome-96x96.png', permanent=True)),
	url(r'^android-chrome-144x144\.png$', RedirectView.as_view(url='/static/servers/favicons/android-chrome-144x144.png', permanent=True)),
	url(r'^android-chrome-192x192\.png$', RedirectView.as_view(url='/static/servers/favicons/android-chrome-192x192.png', permanent=True)),
	url(r'^favicon-16x16\.png$', RedirectView.as_view(url='/static/servers/favicons/favicon-16x16.png', permanent=True)),
    url(r'^manifest\.json$', RedirectView.as_view(url='/static/servers/favicons/manifest.json', permanent=True)),
    url(r'^safari-pinned-tab\.svg$', RedirectView.as_view(url='/static/servers/favicons/safari-pinned-tab.svg', permanent=True)),
	url(r'^mstile-70x70\.png$', RedirectView.as_view(url='/static/servers/favicons/mstile-70x70.png', permanent=True)),
    url(r'^mstile-144x144\.png$', RedirectView.as_view(url='/static/servers/favicons/mstile-144x144.png', permanent=True)),
    url(r'^mstile-150x150\.png$', RedirectView.as_view(url='/static/servers/favicons/mstile-150x150.png', permanent=True)),
	url(r'^mstile-310x150\.png$', RedirectView.as_view(url='/static/servers/favicons/mstile-310x150.png', permanent=True)),
	url(r'^mstile-310x310\.png$', RedirectView.as_view(url='/static/servers/favicons/mstile-310x310.png', permanent=True)),
	url(r'^favicon\.ico$', RedirectView.as_view(url='/static/servers/favicons/favicon.ico', permanent=True)),
	url(r'^browserconfig\.xml$', RedirectView.as_view(url='/static/servers/favicons/browserconfig.xml', permanent=True)),
	
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'', include('page.urls', app_name="page", namespace='page')),
    url(r'^', include('server.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
