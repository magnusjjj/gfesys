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
from profileapi.views.profile.ViewProfileList import ViewProfileList

from models import GfeGroup

urlpatterns = patterns('',
					url(r'^$', ViewProfileList.as_view(profilemodel=GfeGroup), name='index'),
					url(r'^$groups/', ViewProfileList.as_view(profilemodel=GfeGroup), name='grouplist'),
					url('', include("gfegroups.profileurls", namespace="profile")),
				)
