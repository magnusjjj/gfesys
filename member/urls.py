from django.conf.urls import patterns, url


from member.views_d import *

urlpatterns = patterns('',
	url(r'^register$', plain.register, name='register'),
	url(r'^login$', plain.login, name='login'),
	url(r'^logout$', api.logout, name='logout'),
	url(r'^login_post$', api.login_post, name='login_post'),
	url(r'^forgot_post$', api.forgot_post, name='forgot_post'),
	url(r'^register_post$', api.register_post, name='register_post'),
	url(r'^members/(?P<member_id>\d+)/$', community.members_view, name='member'),
url(r'^members', community.members_index, name='members_index'),
	
)
