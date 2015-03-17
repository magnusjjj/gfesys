from django.conf.urls import patterns, url


from page import views

urlpatterns = patterns('',
	url(r'^(?P<page_id>\d+)/$', views.page, name='page'),
	url(r'^edit/(?P<page_id>\d+)/$', views.edit_page, name='edit_page'),
	url(r'^new/$', views.new_page, name='new_page'),
)