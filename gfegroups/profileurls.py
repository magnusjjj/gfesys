# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

#todo: Refactor this, since its pretty much copypasta server/profileurls.py

# This file handles what url's are mapped to what view.
# This is explained pretty well in the django manual:
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

# We do something slightly different though.
# profilemodel=GfeGroup
# Every url that imports functionality from the profileapi needs that. It sends along what type of model to expect.
# Nothing really fancier than that :).

# Check out this list of imports baby. Ain't this a beauty.
from django.conf.urls import url

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

from models import GfeGroup

app_name = "gfegroups"

urlpatterns = [
					   url(r'^volunteer/(?P<profile_id>[0-9]+)/$', ViewVolunteerFor.as_view(profilemodel=GfeGroup), name='volunteer'),
					   url(r'^edit/(?P<profile_id>\d+)/$', EditProfile.as_view(profilemodel=GfeGroup), name='edit'),
					   url(r'^new', EditProfile.as_view(profilemodel=GfeGroup), name='new'),
					   url(r'^managevolunteers/(?P<profile_id>\d+)/$', ViewManageVolunteers.as_view(profilemodel=GfeGroup), name='managevolunteers'),
					   url(r'^editapplicant$', EditApplicant.as_view(profilemodel=GfeGroup), name='editapplicant'),
					   url(r'^viewanswers$', ViewAnswers.as_view(profilemodel=GfeGroup), name='viewanswers'),
					   url(r'^uploadprofileimage/(?P<profile_id>\d+)/$', UploadProfileImage.as_view(profilemodel=GfeGroup), name='uploadprofileimage'),
					   url(r'^updateprofile/(?P<profile_id>\d+)/$', EditProfile.as_view(profilemodel=GfeGroup), name='updateprofileinfo'),
					   url(r'^addpage/(?P<profile_id>\d+)/$', AddPage.as_view(profilemodel=GfeGroup), name='addpage'),
					   url(r'^deletepage/(?P<page_id>\d+)/$', DeletePage.as_view(profilemodel=GfeGroup), name='deletepage'),
					   url(r'^editpage/(?P<page_id>\d+)/$', EditPage.as_view(profilemodel=GfeGroup), name='editpage'),
					   url(r'^(?P<slug>[a-zA-Z\-_0-9]+)/$', ViewProfile.as_view(profilemodel=GfeGroup), name='detail'),
					   url(r'^(?P<slug>[a-zA-Z\-_0-9]+)/(?P<slug_page>[a-zA-Z\-_0-9]+)$', ViewProfile.as_view(profilemodel=GfeGroup), name='detail'),
					   ]
