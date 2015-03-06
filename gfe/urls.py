from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gfe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', include('server.urls')),
    url(r'^servers/', include('server.urls')),
	url(r'^members/', include('member.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
