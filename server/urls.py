# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

# This file handles what url's are mapped to what view.
# This is much better explained in the Django manual,
# and we don't do anything freakier than what is explained in the tutorials. Promise <3
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

import profileapi.views.pages.AddPage
from django.conf.urls import patterns, url

from profileapi.views.profile.UpdateProfile import UpdateProfile
from profileapi.views.profile.ViewProfileList import ViewProfileList
from profileapi.views.profile.EditProfile import EditProfile
from profileapi.views.profile.ViewProfile import ViewProfile
from profileapi.views.profile.UploadProfileImage import UploadProfileImage
from profileapi.views.volunteer.ViewVolunteerFor import ViewVolunteerFor
from profileapi.views.volunteer.ViewManageVolunteers import ViewManageVolunteers
from profileapi.views.volunteer.EditApplicant import EditApplicant
from profileapi.views.volunteer.ViewAnswers import ViewAnswers
from server.views_normal.ViewIndex import ViewIndex
from profileapi.views.pages.EditPage import EditPage
from profileapi.views.pages.AddPage import AddPage
from profileapi.views.pages.DeletePage import DeletePage

from models import Server

urlpatterns = patterns('',
					   url(r'^$', ViewIndex.as_view(), name='index'),
					   url(r'^$servers/', ViewProfileList.as_view(), name='serverlist'),
					   url(r'^volunteer/(?P<server_id>\d+)/$', ViewVolunteerFor.as_view(), name='volunteer'),
					   url(r'^editserver/(?P<server_id>\d+)/$', EditProfile.as_view(), name='editserver'),
					   url(r'^newserver', EditProfile.as_view(), name='newserver'),
					   url(r'^managevolunteers/(?P<server_id>\d+)/$', ViewManageVolunteers.as_view(), name='managevolunteers'),
					   url(r'^servereditapplicant$', EditApplicant.as_view(), name='servereditapplicant'),
					   url(r'^serverviewanswers$', ViewAnswers.as_view(), name='serverviewanswers'),
					   url(r'^uploadserverimage/(?P<server_id>\d+)/$', UploadProfileImage.as_view(), name='uploadserverimage'),
					   url(r'^updateserverinfo/(?P<server_id>\d+)/$', UpdateProfile.as_view(), name='updateserverinfo'),
					   url(r'^addpage/(?P<server_id>\d+)/$', AddPage.as_view(), name='addpage'),
					   url(r'^deletepage/(?P<page_id>\d+)/$', DeletePage.as_view(), name='deletepage'),
					   url(r'^editpage/(?P<page_id>\d+)/$', EditPage.as_view(), name='editpage'),
					   url(r'^(?P<slug>[a-zA-Z\-_0-9]+)/$', ViewProfile.as_view(profilemodel=Server), name='detail'),
					   url(r'^(?P<slug>[a-zA-Z\-_0-9]+)/(?P<slug_page>[a-zA-Z\-_0-9]+)$', ViewProfile.as_view(), name='detail'),
					   )
