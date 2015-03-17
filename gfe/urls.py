from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from ajax_select import urls as ajax_select_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gfe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('server.urls')),
	url(r'^forum', include('spirit.urls', namespace="spirit", app_name="spirit")),
    url(r'^servers/', include('server.urls')),
    url(r'^members/', include('member.urls', app_name="member")),
	url(r'^pages/', include('page.urls', app_name="page")),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^admin/lookups/', include(ajax_select_urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
