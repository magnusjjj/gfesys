# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

# This file handles what url's are mapped to what view.
# This is much better explained in the Django manual,
# and we don't do anything freakier than what is explained in the tutorials. Promise <3
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

import server.groupapi.views.AddPage
from django.conf.urls import patterns, url

import server.groupapi.views.pages.DeletePage
import server.groupapi.views.profile.UpdateProfile
import server.groupapi.views.profile.UploadProfileImage
import server.groupapi.views.volunteer.ServerViewAnswers
import server.groupapi.views.volunteer.ViewManageVolunteers
import server.groupapi.views.volunteer.ViewVolunteerFor
import server.views_normal.ViewIndex
from server import views

urlpatterns = patterns('',
					   url(r'^$', server.views_normal.ViewIndex.ViewIndex.as_view(), name='index'),
					   url(r'^$servers/', server.groupapi.views.profile.ViewServerList.ViewServerList.as_view(), name='serverlist'),
					   url(r'^volunteer/(?P<server_id>\d+)/$', server.groupapi.views.volunteer.ViewVolunteerFor.ViewVolunteerFor.as_view(), name='volunteer'),
					   url(r'^editserver/(?P<server_id>\d+)/$', server.groupapi.views.profile.EditServer.EditServer.as_view(), name='editserver'),
					   url(r'^newserver', server.groupapi.views.profile.EditServer.EditServer.as_view(), name='newserver'),
					   url(r'^managevolunteers/(?P<server_id>\d+)/$', server.groupapi.views.volunteer.ViewManageVolunteers.ViewManageVolunteers.as_view(), name='managevolunteers'),
					   url(r'^servereditapplicant$', server.groupapi.views.volunteer.ServerEditApplicant.ServerEditApplicant.as_view(), name='servereditapplicant'),
					   url(r'^serverviewanswers$', server.groupapi.views.volunteer.ServerViewAnswers.ServerViewAnswers.as_view(), name='serverviewanswers'),
					   url(r'^uploadserverimage/(?P<server_id>\d+)/$', server.groupapi.views.profile.UploadProfileImage.UploadServerImage.as_view(), name='uploadserverimage'),
					   url(r'^updateserverinfo/(?P<server_id>\d+)/$', server.groupapi.views.profile.UpdateProfile.UpdateServerInfo.as_view(), name='updateserverinfo'),
					   url(r'^addpage/(?P<server_id>\d+)/$', server.groupapi.views.pages.AddPage.AddPage.as_view(), name='addpage'),
					   url(r'^deletepage/(?P<page_id>\d+)/$', server.groupapi.views.pages.DeletePage.DeletePage.as_view(), name='deletepage'),
					   url(r'^editpage/(?P<page_id>\d+)/$', server.groupapi.views.pages.EditPage.EditPage.as_view(), name='editpage'),
					   url(r'^rocketchatcreateserverapi$', views.rocketchatcreateserverapi.as_view(), name='rocketchatcreateserverapi'),
					   url(r'^(?P<slug>[a-zA-Z\-]+)/$', server.groupapi.views.profile.ViewDetail.ViewDetail.as_view(), name='detail'),
					   url(r'^(?P<slug>[a-zA-Z\-]+)/(?P<slug_page>[a-zA-Z\-]+)$', server.groupapi.views.profile.ViewDetail.ViewDetail.as_view(), name='detail'),
					   )
