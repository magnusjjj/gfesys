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

import server.views_normal.ViewIndex
import server.views_normal.ViewServerList
from server import views

urlpatterns = patterns('',
					   url(r'^$', server.views_normal.ViewIndex.ViewIndex.as_view(), name='index'),
					   url(r'^$servers/', server.views_normal.ViewServerList.ViewServerList.as_view(), name='serverlist'),
					   url(r'^volunteer/(?P<server_id>\d+)/$', views.ViewVolunteerFor.as_view(), name='volunteer'),
					   url(r'^editserver/(?P<server_id>\d+)/$', views.EditServer.as_view(), name='editserver'),
					   url(r'^newserver', views.EditServer.as_view(), name='newserver'),
					   url(r'^managevolunteers/(?P<server_id>\d+)/$', views.ViewManageVolunteers.as_view(), name='managevolunteers'),
					   url(r'^servereditapplicant$', views.ServerEditApplicant.as_view(), name='servereditapplicant'),
					   url(r'^serverviewanswers$', views.ServerViewAnswers.as_view(), name='serverviewanswers'),
					   url(r'^uploadserverimage/(?P<server_id>\d+)/$', views.UploadServerImage.as_view(), name='uploadserverimage'),
					   url(r'^updateserverinfo/(?P<server_id>\d+)/$', views.UpdateServerInfo.as_view(), name='updateserverinfo'),
					   url(r'^addpage/(?P<server_id>\d+)/$', views.AddPage.as_view(), name='addpage'),
					   url(r'^deletepage/(?P<page_id>\d+)/$', views.DeletePage.as_view(), name='deletepage'),
					   url(r'^editpage/(?P<page_id>\d+)/$', views.EditPage.as_view(), name='editpage'),
					   url(r'^rocketchatcreateserverapi$', views.rocketchatcreateserverapi.as_view(), name='rocketchatcreateserverapi'),
					   url(r'^(?P<slug>[a-zA-Z\-]+)/$', views.ViewDetail.as_view(), name='detail'),
					   url(r'^(?P<slug>[a-zA-Z\-]+)/(?P<slug_page>[a-zA-Z\-]+)$', views.ViewDetail.as_view(), name='detail'),
					   )
