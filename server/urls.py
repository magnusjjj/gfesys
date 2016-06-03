# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

# This file handles what url's are mapped to what view.
# This is much better explained in the Django manual,
# and we don't do anything freakier than what is explained in the tutorials. Promise <3
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

from django.conf.urls import patterns, url

import server.views_normal.AddPage
import server.views_normal.DeletePage
import server.views_normal.EditPage
import server.views_normal.EditServer
import server.views_normal.ServerEditApplicant
import server.views_normal.ServerViewAnswers
import server.views_normal.UpdateServerInfo
import server.views_normal.UploadServerImage
import server.views_normal.ViewDetail
import server.views_normal.ViewIndex
import server.views_normal.ViewManageVolunteers
import server.views_normal.ViewServerList
import server.views_normal.ViewVolunteerFor
from server import views

urlpatterns = patterns('',
					   url(r'^$', server.views_normal.ViewIndex.ViewIndex.as_view(), name='index'),
					   url(r'^$servers/', server.views_normal.ViewServerList.ViewServerList.as_view(), name='serverlist'),
					   url(r'^volunteer/(?P<server_id>\d+)/$', server.views_normal.ViewVolunteerFor.ViewVolunteerFor.as_view(), name='volunteer'),
					   url(r'^editserver/(?P<server_id>\d+)/$', server.views_normal.EditServer.EditServer.as_view(), name='editserver'),
					   url(r'^newserver', server.views_normal.EditServer.EditServer.as_view(), name='newserver'),
					   url(r'^managevolunteers/(?P<server_id>\d+)/$', server.views_normal.ViewManageVolunteers.ViewManageVolunteers.as_view(), name='managevolunteers'),
					   url(r'^servereditapplicant$', server.views_normal.ServerEditApplicant.ServerEditApplicant.as_view(), name='servereditapplicant'),
					   url(r'^serverviewanswers$', server.views_normal.ServerViewAnswers.ServerViewAnswers.as_view(), name='serverviewanswers'),
					   url(r'^uploadserverimage/(?P<server_id>\d+)/$', server.views_normal.UploadServerImage.UploadServerImage.as_view(), name='uploadserverimage'),
					   url(r'^updateserverinfo/(?P<server_id>\d+)/$', server.views_normal.UpdateServerInfo.UpdateServerInfo.as_view(), name='updateserverinfo'),
					   url(r'^addpage/(?P<server_id>\d+)/$', server.views_normal.AddPage.AddPage.as_view(), name='addpage'),
					   url(r'^deletepage/(?P<page_id>\d+)/$', server.views_normal.DeletePage.DeletePage.as_view(), name='deletepage'),
					   url(r'^editpage/(?P<page_id>\d+)/$', server.views_normal.EditPage.EditPage.as_view(), name='editpage'),
					   url(r'^rocketchatcreateserverapi$', views.rocketchatcreateserverapi.as_view(), name='rocketchatcreateserverapi'),
					   url(r'^(?P<slug>[a-zA-Z\-]+)/$', server.views_normal.ViewDetail.ViewDetail.as_view(), name='detail'),
					   url(r'^(?P<slug>[a-zA-Z\-]+)/(?P<slug_page>[a-zA-Z\-]+)$', server.views_normal.ViewDetail.ViewDetail.as_view(), name='detail'),
					   )
