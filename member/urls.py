# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.conf.urls import url

# This file handles what url's are mapped to what view.
# This is much better explained in the Django manual,
# and we don't do anything freakier than what is explained in the tutorials. Promise <3
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

from member.views_d import *

urlpatterns = [
	url(r'^register$', plain.register, name='register'),
	url(r'^login$', plain.login, name='login'),
	url(r'^logout$', api.logout, name='logout'),
	url(r'^login_post$', api.login_post, name='login_post'),
	url(r'^forgot_post$', api.forgot_post, name='forgot_post'),
	url(r'^register_post$', api.register_post, name='register_post'),
	url(r'^become_member$', community.become_member, name='become_member'),
	url(r'^me/$', api.me, name='me'),
	url(r'^members/(?P<member_id>\d+)/$', community.members_view, name='member'),
	url(r'^members', community.members_index, name='members_index'),
]
