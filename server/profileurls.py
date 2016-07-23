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

from profileapi.views.profile.EditProfile import EditProfile
from profileapi.views.profile.ViewProfile import ViewProfile
from profileapi.views.profile.UploadProfileImage import UploadProfileImage
from profileapi.views.volunteer.ViewVolunteerFor import ViewVolunteerFor
from profileapi.views.volunteer.ViewManageVolunteers import ViewManageVolunteers
from profileapi.views.volunteer.EditApplicant import EditApplicant
from profileapi.views.volunteer.ViewAnswers import ViewAnswers
from profileapi.views.pages.EditPage import EditPage
from profileapi.views.pages.AddPage import AddPage
from profileapi.views.pages.DeletePage import DeletePage

from server.models import Server

app_name = "server"

urlpatterns = patterns('',
					   url(r'^volunteer/(?P<profile_id>[0-9]+)/$', ViewVolunteerFor.as_view(profilemodel=Server), name='volunteer'),
					   url(r'^edit/(?P<profile_id>\d+)/$', EditProfile.as_view(profilemodel=Server), name='edit'),
					   url(r'^new', EditProfile.as_view(profilemodel=Server), name='new'),
					   url(r'^managevolunteers/(?P<profile_id>\d+)/$', ViewManageVolunteers.as_view(profilemodel=Server), name='managevolunteers'),
					   url(r'^editapplicant$', EditApplicant.as_view(profilemodel=Server), name='editapplicant'),
					   url(r'^viewanswers$', ViewAnswers.as_view(profilemodel=Server), name='viewanswers'),
					   url(r'^uploadprofileimage/(?P<profile_id>\d+)/$', UploadProfileImage.as_view(profilemodel=Server), name='uploadprofileimage'),
					   url(r'^updateprofile/(?P<profile_id>\d+)/$', EditProfile.as_view(profilemodel=Server), name='updateprofileinfo'),
					   url(r'^addpage/(?P<profile_id>\d+)/$', AddPage.as_view(profilemodel=Server), name='addpage'),
					   url(r'^deletepage/(?P<page_id>\d+)/$', DeletePage.as_view(profilemodel=Server), name='deletepage'),
					   url(r'^editpage/(?P<page_id>\d+)/$', EditPage.as_view(profilemodel=Server), name='editpage'),
					   url(r'^(?P<slug>[a-zA-Z\-_0-9]+)/$', ViewProfile.as_view(profilemodel=Server), name='detail'),
					   url(r'^(?P<slug>[a-zA-Z\-_0-9]+)/(?P<slug_page>[a-zA-Z\-_0-9]+)$', ViewProfile.as_view(profilemodel=Server), name='detail'),
					   )
