# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

# This file handles what url's are mapped to what view.
# This is much better explained in the Django manual,
# and we don't do anything freakier than what is explained in the tutorials. Promise <3
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

from django.conf.urls import patterns, url, include
from server.views_normal.ViewIndex import ViewIndex
from profileapi.views.profile.UpdateProfile import UpdateProfile
from profileapi.views.profile.ViewProfileList import ViewProfileList
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

from models import Server

urlpatterns = patterns('',
					url(r'^$', ViewIndex.as_view(), name='index'),
					url(r'^$servers/', ViewProfileList.as_view(), name='serverlist'),
					url('', include("server.profileurls", namespace="profile")),
				)
