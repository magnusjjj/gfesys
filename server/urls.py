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


from server import views

urlpatterns = patterns('',
    url(r'^$', views.ViewIndex.as_view(), name='index'),
	url(r'^(?P<server_id>\d+)/$', views.ViewDetail.as_view(), name='detail'),
	url(r'^volunteer/(?P<server_id>\d+)/$', views.ViewVolunteerFor.as_view(), name='volunteer'),
	url(r'^editserver/(?P<server_id>\d+)/$', views.EditServer.as_view(), name='editserver'),
	url(r'^newserver$', views.EditServer.as_view(), name='newserver'),
	url(r'^managevolunteers/(?P<server_id>\d+)/$', views.ViewManageVolunteers.as_view(), name='managevolunteers'),
	url(r'^servereditapplicant$', views.ServerEditApplicant.as_view(), name='servereditapplicant'),
	url(r'^serverviewanswers$', views.ServerViewAnswers.as_view(), name='serverviewanswers'),
	url(r'^uploadserverimage/(?P<server_id>\d+)/$', views.UploadServerImage.as_view(), name='uploadserverimage'),
	url(r'^updateserverinfo/(?P<server_id>\d+)/$', views.UpdateServerInfo.as_view(), name='updateserverinfo'),
)
